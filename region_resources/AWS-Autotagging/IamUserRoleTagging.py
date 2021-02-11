import json
import boto3
import os
import sys
import uuid
import time
import TaggingLogic
from botocore.config import Config
from urllib.parse import unquote_plus


def ThrottlingExceptionHandling():
        time.sleep(3)
        print("Inside ThrottlingExceptionHandling")

        
def iam_user_role_tag_logic(global_tag_key_val_list):
 print ("Start to Tag IAM Users and Role with Global tags, Company specific tags are not applied in IAM.")

 UserName_arr = []
 User_arr = []
 role_arr = []
 rolename_arr = []
 role_count_res = []
 usr_count_res = []
 iam_tagged = 0
 iam_not_tagged = 0 
 iam_con_cli = boto3.client(service_name="iam")
 # logic to get Users
 paginator = iam_con_cli.get_paginator('list_users')
 for each_paginat in paginator.paginate():
    for each_item in each_paginat['Users']:
        User_arr.append(each_item)
        UserName_arr.append(each_item['UserName'])
 
 for user in UserName_arr:
    try:
        res = iam_con_cli.tag_user(UserName=user, Tags= global_tag_key_val_list)
        #print(res)
        iam_tagged+=1
        usr_count_res.append(user)
    except Exception as e:
            print("Not Tagged UserName and Error:: ", e)
            iam_not_tagged+=1
 print("Added tag to UserName List::",usr_count_res )
 print("Users added with global tag count:", iam_tagged, "and Not tagged:", iam_not_tagged)

# logic for apply tag on RoleName   
 iam_tagged = 0
 iam_not_tagged = 0 
 
 paginator = iam_con_cli.get_paginator('list_roles')
 
 
 for each_paginat in paginator.paginate():
    for each_item in each_paginat['Roles']:
       try: 
        role_arr.append(each_item)
        rolename_arr.append(each_item['RoleName'])

       except Exception as e:
        ExceptionName = str(e)
        if TaggingLogic.check(ExceptionName, 'Throttling'):
            ThrottlingExceptionHandling()
        else:
            print("New error: ", e)
            #not_tagged_res = not_tagged_res + 1
      
       
 for role in rolename_arr:
    try:
        res =iam_con_cli.tag_role(RoleName=role, Tags= global_tag_key_val_list)
        #print(res)
        iam_tagged+=1
        role_count_res.append(role)
    except Exception as e:
        ExceptionName = str(e)
        if TaggingLogic.check(ExceptionName, 'Throttling'):
            ThrottlingExceptionHandling()

        else:
            print("Not Tagged RoleName and Error:: ", e)
            iam_not_tagged = iam_not_tagged + 1
 
#####################################################################################################################
 print("Added tag to RoleName List::",role_count_res )
 print("Roles added with global tag:", iam_tagged, "and Not tagged:", iam_not_tagged)
 return True
