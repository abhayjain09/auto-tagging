import json
import boto3
import os, sys, uuid
import time
import GetResource
import TaggingLogic
from botocore.config import Config
from urllib.parse import unquote_plus
import IamUserRoleTagging

#Logic to get AWS account id
account_id = boto3.client('sts').get_caller_identity().get('Account')
np_sers_ids = []


runtime_region = os.environ['AWS_REGION']
RegionID =  [runtime_region]
account_id = boto3.client('sts').get_caller_identity().get('Account')
BucketName = 'autotag-bucket-'+account_id
Bucket_region = 'us-east-1'



#RegionID = ['ap-southeast-1','us-east-1','us-west-2','us-west-2','eu-central-1','eu-west-1']
#RegionID = ['ap-southeast-1','us-east-1','us-west-2','us-west-2','eu-central-1','eu-west-1','us-west-2','eu-west-3','eu-north-1','us-west-1','sa-east-1','ca-central-1','ap-south-1','us-east-2','ap-southeast-2','eu-west-2']

# check substring in string
def check(string, sub_str):
    string = string.lower()
    sub_str = sub_str.lower()
    if (string.find(sub_str) == -1):
        return(False)
    else:
        return(True)


def ThrottlingExceptionHandling():
        time.sleep(3)
        print("Inside ThrottlingExceptionHandling")

def lambda_handler(event, context):
 print(event)
 chuck = []
 tagged_res = 0
 not_tagged_res=0
 total_get_resource = []
 
 ##################################################################################################################################################
 #Logic to get Global tag from S3 bucket 
 Global_tag_var = {}
 s3_con_res = boto3.resource('s3')
 s3_con_cli = boto3.client(service_name="s3", region_name= Bucket_region)

 for key in s3_con_cli.list_objects(Bucket=BucketName , Prefix = 'Global-tag/global.json')['Contents']:
    itemname=(key['Key'])
    try:
     obj = s3_con_res.Object(BucketName, itemname)
     body = obj.get()['Body'].read().decode() 
     Global_tag_var =json.loads(body)
     #print(Global_tag_var)
    except:
        print("global.json not found in S3 bucket, please check the file. No global tags applied.")

 # Get All resources ARN 
 for region in RegionID:
    np_sers_ids = [] 
    total_get_resource = []
    np_sers_ids = GetResource.get_resource(region)
    #print("**********************************",np_sers_ids)
    
    resgrptag_con_cli = boto3.client(service_name='resourcegroupstaggingapi', region_name=region)
    paginator = resgrptag_con_cli.get_paginator('get_resources')  
    for each_paginat in paginator.paginate():
         for each in each_paginat['ResourceTagMappingList']:
           total_get_resource.append(each['ResourceARN'])

    np_sers_ids = total_get_resource + np_sers_ids
    np_sers_ids = list(dict.fromkeys(np_sers_ids))


##################################################################################################################################################


##################################################################################################################

 # Logic to get list of all resources that already have global tag value.

    Np_server_id_count = len(np_sers_ids)
    print("Total resources count in region ", region,":", len(np_sers_ids))
 
    for each_paginat in paginator.paginate():
      for each in each_paginat['ResourceTagMappingList']:
          
          remv_var = 0
          for tag_key in each['Tags']:
              for each_glb_key, each_glb_val in Global_tag_var.items():
                if (tag_key['Key'] == each_glb_key  and tag_key['Value'] == each_glb_val ):
                    remv_var+=1
        
          if remv_var == len(Global_tag_var):
              #print(each['ResourceARN'])
              try:
                 np_sers_ids.remove(each['ResourceARN'])
              except:
                  print("")
    print("Remove already tagged resources with global tag, Remaining count: ", len(np_sers_ids),"that need to tag")
 
###########################^^^^^^^^^^^^^^^^^^^^^^^^#########################
# logic to tag remaining resources with global tags
  
    glb_tagged_res, glb_not_tagged_res = TaggingLogic.tagging_logic(region, np_sers_ids, Global_tag_var)
    print("Resources tagged with global tags:", Np_server_id_count,", Not tagged:", glb_not_tagged_res)




###############################################################################################################
 #region = "us-west-2"
 print("Company Specific App tagging Started")
 s3_con_res = boto3.resource('s3')
 s3_con_cli = boto3.client(service_name="s3", region_name=Bucket_region)
 #sers_ids = []
 sers_arn= []
 #Tag_var={}
 #add_tag = []
 not_valid_arn = []
 
 for region in RegionID:
  sers_arn= []
  not_valid_arn = []
  resgrptag_con_cli = boto3.client(service_name='resourcegroupstaggingapi', region_name= region)
  paginator = resgrptag_con_cli.get_paginator('get_resources')
  for each_paginat in paginator.paginate():
     for each in each_paginat['ResourceTagMappingList']:
        sers_arn.append(each)
        #print(each)
  #print("@@@@@@@@@@@",sers_arn)
  for key in s3_con_cli.list_objects(Bucket=BucketName, Prefix = 'App-tag/',)['Contents']:
     sers_ids = []
     add_tag = []
     Tag_var={}
     app_tag_add_count=0
     app_tag_not_add_count=0
     itemname=(key['Key'])
     #print(itemname)
     try:
      obj = s3_con_res.Object(BucketName, itemname)   
      body = obj.get()['Body'].read().decode() 
      #print(body)
      Tag_var =json.loads(body)
      tag_var_persent = True
      tag_var_persent = check(str(Tag_var),'Company')  # Check in App tag file "Company" tag present or not.
     except:
      tag_var_persent=False
    
     if tag_var_persent:
      company_tag = Tag_var['Company']
      company_tag_small_case = company_tag.lower()
      for each in sers_arn:
           for all_tag in each['Tags']:
              if (all_tag['Key'] == 'Company' or all_tag['Key'] == 'company'):
                  temp = all_tag['Value']
                  temp = temp.lower()
                  if (temp == company_tag_small_case):
                     add_tag.append(each['ResourceARN'])
      app_tag_total_count = len(add_tag)
                 
 # Logic to remove Resources that already have same app tags value.

      for each in sers_arn:  
        remv_var = 0
        for tag_key in each['Tags']:
              for each_app_key, each_app_val in Tag_var.items():
                if (tag_key['Key'] == each_app_key  and tag_key['Value'] == each_app_val):
                    remv_var+=1
        
        if remv_var == len(Tag_var):
              #print(each['ResourceARN'])
              try:
                 add_tag.remove(each['ResourceARN'])
              except:
                  print("")
      #print("after already app tagged resources remove:", len(add_tag))

      try:   
             print("Adding tag for Company:  ",Tag_var['Company'])
             app_tag_add_count, app_tag_not_add_count = TaggingLogic.tagging_logic(region, add_tag, Tag_var)
             print("For ",Tag_var['Company']," Company Specific tag added to resource count:", app_tag_total_count," and not added:",(app_tag_not_add_count))
     
      except:
             print("")



######################################################################################################################
 # Convert global tag value from dict to List, because IAM addtag method do not support dict as an input.
 global_tag_key_val_list =[]
 for key, value in Global_tag_var.items():
    temp = {'Key':key, 'Value': value}
    global_tag_key_val_list.append(temp)
 
################################################################################################################
 
 try:
   responce = IamUserRoleTagging.iam_user_role_tag_logic(global_tag_key_val_list)
 except Exception as e:
     print(e)
 