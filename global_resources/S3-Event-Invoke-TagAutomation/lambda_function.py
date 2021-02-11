import boto3
import json

def lambda_handler(event, context):
   #change region_name as per the destination lambda function region
   #RegionID = ['ap-southeast-1','ap-northeast-1','us-east-1','us-west-2','eu-central-1','eu-west-1',]
   client = boto3.client('ec2')
   RegionID = []
   response = client.describe_regions()
   for each in response['Regions']:
     RegionID.append(each['RegionName'])
   
   payload = {"message": "S3 bucket has changed and invoked Lambda for Autotagging or Invoked by cloudwatch event"}
   for region in RegionID: 
        lambda_con_cli = boto3.client(service_name = "lambda", region_name= region)
        #For InvocationType = "Event"
        try:
         resp = lambda_con_cli.invoke(FunctionName = "Resources-Tag-Automation", InvocationType = "Event", Payload = json.dumps(payload))
         print(resp)
        except:
          print("")

   return 'Thanks'
