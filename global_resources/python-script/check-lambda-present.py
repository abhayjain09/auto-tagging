import boto3
import json

aws_mag_con=boto3.session.Session()
lambda_con_cli = aws_mag_con.client(service_name='lambda',region_name="us-east-1")
#ec2_con_cli =aws_mag_con.client(service_name="ec2",region_name="us-east-1")
#s3_con_res = aws_mag_con.resource('s3')
#s3_con_cli = aws_mag_con.client(service_name="s3",region_name="us-east-1")
ec2_con_cli = aws_mag_con.client('ec2')
RegionID = []
response = ec2_con_cli.describe_regions()
for each in response['Regions']:
    RegionID.append(each['RegionName'])

i = False
for each in RegionID:
 lambda_con_cli = aws_mag_con.client(service_name='lambda',region_name=each)
 #print(each)
 try:
  response = lambda_con_cli.get_function(FunctionName='Resources-Tag-Automation')
  i = True
  break
 except:
  i = False
print(i)