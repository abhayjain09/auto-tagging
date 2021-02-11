import json
import boto3
import os
import sys
import uuid
import time
from botocore.config import Config
from urllib.parse import unquote_plus

tagged_res = 0
not_tagged_res = 0

def check(string, sub_str):
    string = string.lower()
    sub_str = sub_str.lower()
    if (string.find(sub_str) == -1):
        return(False)
    else:
        return(True)

        
def ThrottlingExceptionHandling(region, ResourceList, tag_var):
        print("Inside ThrottlingExceptionHandling")
        time.sleep(3)
        TagResourcesLogic(region, each_new_chunk, tag_var)
        

def InvalidParameterExceptionHandling(region, ResourceList, tag_var):
    list_lenth = len(ResourceList)
    global not_tagged_res
    if (list_lenth > 1):
        chunk_size = int(list_lenth/2)
        new_chuck = [ResourceList[i:i + chunk_size] for i in range(0, len(ResourceList), chunk_size)]
        #print("List lenght: ", list_lenth, "-->",new_chuck)
        for each_new_chunk in new_chuck:
           TagResourcesLogic(region, each_new_chunk, tag_var)

    else:
        print("Not Added tags Resource list::",ResourceList, "::: got InvalidParameter Exception.")
        not_tagged_res = not_tagged_res + 1
        
    
    #return total_tag, not_tagged_res


def TagResourcesLogic(region, ResourceList, tag_var):
    global tagged_res
    global not_tagged_res

    
    try:
        resgrptag_con_cli = boto3.client(service_name='resourcegroupstaggingapi', region_name=region)
        response = resgrptag_con_cli.tag_resources(ResourceARNList=ResourceList, Tags=tag_var) 
        print("Added tags Resource list::",ResourceList)
        tagged_res = tagged_res + len(ResourceList)
    except Exception as e:
        ExceptionName = str(e)
        if check(ExceptionName, 'InvalidParameterException'):
            InvalidParameterExceptionHandling(region, ResourceList, tag_var)

        elif check(ExceptionName, 'Throttling'):
            ThrottlingExceptionHandling(region, ResourceList, tag_var)

        else:
            print("New Error found: ", e)
            not_tagged_res = not_tagged_res + 1

    #return len(ResourceList), not_tagged_res


def tagging_logic(region, remaining_res, tag_var):
  global tagged_res
  global not_tagged_res
  tagged_res = 0
  not_tagged_res = 0
  chunk = []
  # remaining_res = np_sers_ids
  not_valid_arn = []
  # region = "us-west-2"
  resgrptag_con_cli = boto3.client(service_name='resourcegroupstaggingapi', region_name=region)
  chuck = [remaining_res[i:i + 20] for i in range(0, len(remaining_res), 20)]
  for each in chuck:
     time.sleep(1)
     try:

            TagResourcesLogic(region, each, tag_var)

     except Exception as e:
         #print("error",e)
         not_tagged_res = not_tagged_res + 1
  
  return tagged_res, not_tagged_res