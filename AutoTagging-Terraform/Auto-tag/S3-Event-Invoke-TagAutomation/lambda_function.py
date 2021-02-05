import boto3
import json

def lambda_handler(event, context):
   #change region_name as per the destination lambda function region
   #RegionID = ['ap-southeast-1','ap-northeast-1','us-east-1','us-west-2','eu-central-1','eu-west-1',]
   RegionID = ['ap-south-1']
   payload = {"message": "S3 bucket has changed and invoked Lambda for Autotagging."}
   for region in RegionID:
        lambda_con_cli = boto3.client(service_name = "lambda", region_name= region)
        
        #For InvocationType = "Event"
        resp = lambda_con_cli.invoke(FunctionName = "Resources-Tag-Automation", InvocationType = "Event", Payload = json.dumps(payload))
        print(resp)

   return 'Thanks'
