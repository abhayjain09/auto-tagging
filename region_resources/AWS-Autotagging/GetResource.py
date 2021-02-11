import json
import boto3
import os, sys, uuid
import time
from botocore.config import Config
from urllib.parse import unquote_plus
account_id = boto3.client('sts').get_caller_identity().get('Account')
np_sers_ids = []

#RegionID = ['ap-southeast-1','us-east-1','us-west-2','us-west-2','eu-central-1','eu-west-1']

#RegionID = ['ap-southeast-1','us-east-1','us-west-2','us-west-2','eu-central-1','eu-west-1','us-west-2','eu-west-3','eu-north-1','us-west-1','sa-east-1','ca-central-1','ap-south-1','us-east-2','ap-southeast-2','eu-west-2']

def get_resource(region):
    np_sers_ids = []
    region_name = region
    each_region = region
    ## logic to get CertificateArn
    acm_con_cli = boto3.client(service_name='acm', region_name=each_region)
    
    paginator = acm_con_cli.get_paginator('list_certificates')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['CertificateSummaryList']:
            np_sers_ids.append(each_item['CertificateArn'])
########################################################################################################

    # logic to get get_domain_names
    apigateway_con_cli = boto3.client(service_name='apigateway', region_name=each_region)
    
    paginator = apigateway_con_cli.get_paginator('get_domain_names')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['items']:
            arn = 'arn:aws:apigateway:'+ each_region+'::/domainnames/'+ each_item['domainName']
            np_sers_ids.append(arn)

    #restapis
    paginator = apigateway_con_cli.get_paginator('get_rest_apis')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['items']:
            #print(co, each_item['domainName'])
            #arn:aws:apigateway:us-east-1::/restapis/vuytmu7ba0/stages/Prod
            arn = 'arn:aws:apigateway:'+ each_region+'::/restapis/'+ each_item['id']
            np_sers_ids.append(arn)
########################################################################################################

    cf_con_cli = boto3.client(service_name='cloudformation', region_name=each_region)
      # logic for apply tag on describe_stacks  
    paginator = cf_con_cli.get_paginator('describe_stacks')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Stacks']:
            np_sers_ids.append(each_item['StackId'])

########################################################################################################

    CloudTrail_con_cli = boto3.client(service_name='cloudtrail', region_name=each_region)
    paginator = CloudTrail_con_cli.get_paginator('list_trails')
    for each_paginat in paginator.paginate():
        for each_item in CloudTrail_con_cli.list_trails()['Trails']:
            np_sers_ids.append(each_item['TrailARN']) 
      
########################################################################################################

    cloudwatch_con_cli = boto3.client(service_name='cloudwatch', region_name=each_region)
    paginator = cloudwatch_con_cli.get_paginator('describe_alarms')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['MetricAlarms']:
           np_sers_ids.append(each_item['AlarmArn'])

#########################################################################################################

    cognito_idp_con_cli= boto3.client(service_name='cognito-idp', region_name=each_region)
    # logic for list cognito_idp_con_cli
    for each_item in cognito_idp_con_cli.list_user_pools(MaxResults=60)['UserPools']:
        #arn:aws:cognito-idp:eu-west-1:274138180186:userpool/eu-west-1_9id8ECwvg
        arn = 'arn:aws:cognito-idp:'+each_region+':'+account_id+':userpool/'+each_item['Id']
        np_sers_ids.append(arn)
#########################################################################################################
    try:
     config_con_cli = boto3.client(service_name='config', region_name=each_region)
     paginator = config_con_cli.get_paginator('describe_config_rules')
     for each_paginat in paginator.paginate():
         for each_item in each_paginat['ConfigRules']:
             np_sers_ids.append(each_item['ConfigRuleArn'])
    except:
        print("")
#########################################################################################################


    DynamoDB_con_cli = boto3.client(service_name='dynamodb', region_name=each_region)
    paginator = DynamoDB_con_cli.get_paginator('list_tables')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['TableNames']:
            Db_ARN= "arn:aws:dynamodb:"+each_region+':'+account_id+":table/"+each_item
            np_sers_ids.append(Db_ARN)

#########################################################################################################

    ec2_con_cli =boto3.client(service_name="ec2",region_name=each_region)

    # Logic for list dhcp_options.     
    paginator = ec2_con_cli.get_paginator('describe_dhcp_options')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DhcpOptions']:
            #logic to build ARN of DSCP option
            dhcp_arn= 'arn:aws:ec2:'+each_region+':' + account_id +':dhcp-options/'+ each_item['DhcpOptionsId']
            np_sers_ids.append(dhcp_arn)
    

    #Logic for Get list of EIP AllocationID, not found paginator
    for each_item in ec2_con_cli.describe_addresses()['Addresses']:
        #arn:aws:ec2:ap-southeast-1:’ + account_id +’:elastic-ip/eipalloc-000b2903357113b5e
        Eip_arn = 'arn:aws:ec2:'+each_region+':' + account_id +':elastic-ip/'+ each_item['AllocationId']
        np_sers_ids.append(Eip_arn)

    # Logic for Get list of EC2 AMI IDs and images owned by me, paginator not found 
    owneridfilter = [{'Name': 'owner-id', 'Values': [account_id]}]
    for each_item in ec2_con_cli.describe_images(Filters = owneridfilter)['Images']:
        #arn:aws:ec2:ap-southeast-1:’ + account_id +’:image/ami-0cf16ddc1bce7cb9a
        image_arn = 'arn:aws:ec2:'+each_region+':' + account_id +':image/'+ each_item['ImageId']
        np_sers_ids.append(image_arn)
        

    #Logic for Get list of EC2 instanceID
    paginator = ec2_con_cli.get_paginator('describe_instances')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Reservations']:
            for each_in in each_item['Instances']:
                #arn:aws:ec2:ap-southeast-1:’ + account_id +’:instance/i-0057bc1c6d912dcc0
                instance_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':instance/'+ each_in['InstanceId']
                np_sers_ids.append(instance_arn)

    # Logic for Get list of EC2 InternetGatewayId
    paginator = ec2_con_cli.get_paginator('describe_internet_gateways')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['InternetGateways']:
            igw_arn= 'arn:aws:ec2:'+ each_region +':' + account_id +':internet-gateway/'+ (each_item['InternetGatewayId'])
            np_sers_ids.append(igw_arn)
            #arn:aws:ec2:us-west-2:’ + account_id +’:internet-gateway/igw-098993578890b0351

    # Logic for Get list of EC2 NetworkAclId
    paginator = ec2_con_cli.get_paginator('describe_network_acls')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['NetworkAcls']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:network-acl/acl-0372e94781bebd77b
            Nacl_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':network-acl/' + each_item['NetworkAclId']
            np_sers_ids.append(Nacl_arn)
         
    # Logic for Get list of EC2 Network interfaces
    paginator = ec2_con_cli.get_paginator('describe_network_interfaces')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['NetworkInterfaces']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:network-interface/eni-0791d96c7fc2f2645
            Nint_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':network-interface/' + each_item['NetworkInterfaceId']
            np_sers_ids.append(Nint_arn)
         
    # Logic for Get list of EC2 describe_route_tables RouteTableId
    paginator = ec2_con_cli.get_paginator('describe_route_tables')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['RouteTables']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:route-table/rtb-04663ca6a020929da
            RT_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':route-table/' + each_item['RouteTableId']
            np_sers_ids.append(RT_arn)
            
    # Logic for Get list of EC2 describe_security_groups GroupId

    paginator = ec2_con_cli.get_paginator('describe_security_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['SecurityGroups']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:security-group/sg-025eb8f3d277d3108
            sg_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':security-group/' + each_item['GroupId']
            np_sers_ids.append(sg_arn)
         
    # Logic for Get list of EC2 Snapshot_ID
    paginator = ec2_con_cli.get_paginator('describe_snapshots')
    for each_paginat in paginator.paginate(OwnerIds=[account_id]):
        for each_item in each_paginat['Snapshots']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:snapshot/snap-0618c0fe924a9f367
            snap_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':snapshot/' + each_item['SnapshotId']
            np_sers_ids.append(snap_arn)

    # Logic for Get list of EC2 describe_subnets SubnetId
    for each_item in ec2_con_cli.describe_subnets()['Subnets']:
         #arn:aws:ec2:us-west-2:’ + account_id +’:subnet/subnet-0b652cb32f80c4539
         subnetARN= 'arn:aws:ec2:'+ each_region + ':' + account_id +':subnet/' + each_item['SubnetId']
         np_sers_ids.append(subnetARN)
         
    # Logic for Get list of EC2 describe_volumes VolumeId
    paginator = ec2_con_cli.get_paginator('describe_volumes')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Volumes']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:volume/vol-0fd9b4a5f6e18c5f8
            vol_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':volume/' + each_item['VolumeId']
            np_sers_ids.append(vol_arn)

    #Logic for Get list of EC2 VPC_ID
    paginator = ec2_con_cli.get_paginator('describe_vpcs')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Vpcs']:
            #arn:aws:ec2:us-west-2:’ + account_id +’:vpc/vpc-049091f95f86d21e3
            vpc_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':vpc/' + each_item['VpcId']
            np_sers_ids.append(vpc_arn)
        
    # Logic for Get list of describe_vpn_gateways
    for each_item in ec2_con_cli.describe_vpn_gateways()['VpnGateways']:
        #arn:aws:ec2:us-west-2:’ + account_id +’:vpn-gateway/vgw-064174556e24b0561
        vpngw_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':vpn-gateway/' + each_item['VpnGatewayId']
        np_sers_ids.append(vpngw_arn)
        
    # Logic for Get list of EC2 NatGatewayId
    paginator = ec2_con_cli.get_paginator('describe_nat_gateways')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['NatGateways']:
            #arn:aws:ec2:eu-west-1:’ + account_id +’:natgateway/nat-0a67a769986fe69d3
            nat_arn= 'arn:aws:ec2:'+ each_region + ':' + account_id +':natgateway/' + each_item['NatGatewayId']
            np_sers_ids.append(nat_arn)

    # Logic for Get list of describe_transit_gateways
    paginator = ec2_con_cli.get_paginator('describe_transit_gateways')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['TransitGateways']:
            np_sers_ids.append(each_item['TransitGatewayArn'])

    # Logic for Get list of describe_transit_gateway_vpc_attachments
    paginator = ec2_con_cli.get_paginator('describe_transit_gateway_vpc_attachments')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['TransitGatewayVpcAttachments']:
            tgw_att_arn= 'arn:aws:ec2:' + each_region + ':' + account_id +':transit-gateway-attachment/'+ each_item['TransitGatewayAttachmentId']
            #arn:aws:ec2:ap-southeast-1:’ + account_id +’:transit-gateway-attachment/tgw-attach-034a48057fcf8c1f3
            np_sers_ids.append(tgw_att_arn)

    # Logic for Get list of VpcEndpoints
    paginator = ec2_con_cli.get_paginator('describe_vpc_endpoints')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['VpcEndpoints']:
            vpcep_att_arn= 'arn:aws:ec2:' + each_region + ':' + account_id +':vpc-endpoint/'+ each_item['VpcEndpointId']
            #arn:aws:ec2:us-west-2:’ + account_id +’:vpc-endpoint/vpce-024c34a99fca82e54
            np_sers_ids.append(vpcep_att_arn)
         

    # Logic for Get list of VpcPeeringConnections
    paginator = ec2_con_cli.get_paginator('describe_vpc_peering_connections')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['VpcPeeringConnections']:
            vpcpeer_arn= 'arn:aws:ec2:' + each_region + ':' + account_id +':vpc-peering-connection/'+ each_item['VpcPeeringConnectionId']
            #arn:aws:ec2:us-east-1:’ + account_id +’:vpc-peering-connection/pcx-0e02805044a49b0d9
            np_sers_ids.append(vpcpeer_arn)

    # Logic for Get list of VpcPeeringConnections
    paginator = ec2_con_cli.get_paginator('describe_vpc_peering_connections')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['VpcPeeringConnections']:
            vpcep_att_arn= 'arn:aws:ec2:' + each_region + ':' + account_id +':vpc-peering-connection/'+ each_item['VpcPeeringConnectionId']
            #arn:aws:ec2:us-east-1:’ + account_id +’:vpc-peering-connection/pcx-0e02805044a49b0d9
            np_sers_ids.append(vpcep_att_arn)

    # Logic for Get list of VpcPeeringConnections
    for each_item in ec2_con_cli.describe_vpn_gateways()['VpnGateways']:
        #arn:aws:ec2:us-west-2:’ + account_id +’:vpn-gateway/vgw-064174556e24b0561
        vpn_gw_arn = 'arn:aws:ec2:' + each_region + ':' + account_id +':vpn-gateway/'+ each_item['VpnGatewayId']
        np_sers_ids.append(vpn_gw_arn)

##################################################################################################################################################

    ecs_con_cli = boto3.client(service_name='ecs', region_name=each_region)

    #logic to list_clusters
    paginator = ecs_con_cli.get_paginator('list_clusters')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['clusterArns']:
            np_sers_ids.append(each_item)
    
    #logic to taskDefinitionArns
    paginator = ecs_con_cli.get_paginator('list_task_definitions')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['taskDefinitionArns']:
            np_sers_ids.append(each_item)

##################################################################################################################################################

    elasticbeanstalk_con_cli = boto3.client(service_name='elasticbeanstalk', region_name=each_region)
    #logic to get ApplicationVersions
    paginator = elasticbeanstalk_con_cli.get_paginator('describe_application_versions')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['ApplicationVersions']:
            np_sers_ids.append(each_item['ApplicationVersionArn'])
    
    #logic to get Application
    for each in elasticbeanstalk_con_cli.describe_applications()['Applications']:
        np_sers_ids.append(each['ApplicationArn'])


    #logic to get DescribeEnvironments
    paginator = elasticbeanstalk_con_cli.get_paginator('describe_environments')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Environments']:
            np_sers_ids.append(each_item['EnvironmentArn'])

##################################################################################################################################################

    elbv2_con_cli = boto3.client(service_name='elbv2', region_name=each_region)
    #logic to get LoadBalancerArn
    paginator = elbv2_con_cli.get_paginator('describe_load_balancers')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['LoadBalancers']:
            np_sers_ids.append(each_item['LoadBalancerArn'])

    #logic to get TargetGroupArn
    paginator = elbv2_con_cli.get_paginator('describe_target_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['TargetGroups']:
            np_sers_ids.append(each_item['TargetGroupArn'])

##################################################################################################################################################

    events_con_cli = boto3.client(service_name='events', region_name=each_region)
    paginator = events_con_cli.get_paginator('list_rules')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Rules']:
            np_sers_ids.append(each_item['Arn'])

##################################################################################################################################################

    fsx_con_cli = boto3.client(service_name='fsx', region_name=each_region)
    #logic to get Backups
    paginator = fsx_con_cli.get_paginator('describe_backups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Backups']:
            np_sers_ids.append(each_item['ResourceARN'])

##################################################################################################################################################

    glue_con_cli = boto3.client(service_name='glue', region_name=each_region)
    paginator = glue_con_cli.get_paginator('get_crawlers')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Crawlers']:
            #arn:aws:glue:us-east-1:274138180186:crawler/MetaData
            cra_arn = 'arn:aws:glue:' + each_region + ':' + account_id +':crawler/'+ each_item['Name']
            np_sers_ids.append(cra_arn)

    ###### need to check ARN that might be wrong
    # logic to get Jobs
    paginator = glue_con_cli.get_paginator('get_jobs')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Jobs']:
            job_arn = 'arn:aws:glue:' + each_region + ':' + account_id +':job/'+ each_item['Name']
            np_sers_ids.append(job_arn)

##################################################################################################################################################

    kms_con_cli = boto3.client(service_name='kms', region_name=each_region)
    paginator = kms_con_cli.get_paginator('list_keys')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Keys']:
            np_sers_ids.append(each_item['KeyArn'])

##################################################################################################################################################

    lambda_con_cli = boto3.client(service_name="lambda", region_name=each_region)
    paginator = lambda_con_cli.get_paginator('list_functions')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Functions']:
            np_sers_ids.append(each_item['FunctionArn'])

##################################################################################################################################################

    rds_con_cli = boto3.client(service_name="rds", region_name=each_region)

    # logic to get ReservedDBInstanceArn
    paginator = rds_con_cli.get_paginator('describe_reserved_db_instances')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['ReservedDBInstances']:
            np_sers_ids.append(each_item['ReservedDBInstanceArn'])

    # logic to get DBSecurityGroupArn 
    paginator = rds_con_cli.get_paginator('describe_db_security_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBSecurityGroups']:
            np_sers_ids.append(each_item['DBSecurityGroupArn'])

    #logic to get DBClusterArn
    paginator = rds_con_cli.get_paginator('describe_db_clusters')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBClusters']:
            np_sers_ids.append(each_item['DBClusterArn'])

    #logic for apply tag on DB_instane  
    paginator = rds_con_cli.get_paginator('describe_db_instances')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBInstances']:
            np_sers_ids.append(each_item['DBInstanceArn'])

    #logic for apply tag on DBSnapshots and add_tags_to_resource() is only accept ResourceName='string' not 'list'
    paginator = rds_con_cli.get_paginator('describe_db_snapshots')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBSnapshots']:
            np_sers_ids.append(each_item['DBSnapshotArn'])

    #logic for apply tag on DBParameterGroupArn and add_tags_to_resource() is only accept ResourceName='string' not 'list'
    paginator = rds_con_cli.get_paginator('describe_db_parameter_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBParameterGroups']:
            np_sers_ids.append(each_item['DBParameterGroupArn'])
    
    #logic for apply tag on DBClusterParameterGroupArn and add_tags_to_resource() is only accept ResourceName='string' not 'list' 
    paginator = rds_con_cli.get_paginator('describe_db_cluster_parameter_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBClusterParameterGroups']:
            np_sers_ids.append(each_item['DBClusterParameterGroupArn'])

    #logic for apply tag on OptionGroupArn and add_tags_to_resource() is only accept ResourceName='string' not 'list' 
    paginator = rds_con_cli.get_paginator('describe_option_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['OptionGroupsList']:
            np_sers_ids.append(each_item['OptionGroupArn'])

    #logic for apply tag on DBSubnetGroupArn and add_tags_to_resource() is only accept ResourceName='string' not 'list' 
    paginator = rds_con_cli.get_paginator('describe_db_subnet_groups')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBSubnetGroups']:
            np_sers_ids.append(each_item['DBSubnetGroupArn'])
    
    #logic for apply tag on DBClusterArn and add_tags_to_resource() is only accept ResourceName='string' not 'list' 
    paginator = rds_con_cli.get_paginator('describe_db_clusters')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['DBClusters']:
            np_sers_ids.append(each_item['DBClusterArn'])
    
##################################################################################################################################################

    route53_con_cli = boto3.client(service_name='route53', region_name=each_region)
    paginator = route53_con_cli.get_paginator('list_health_checks')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['HealthChecks']:
            #arn:aws:route53:::healthcheck/a6b887c9-34f3-4935-b844-6a24c404f669
            arn_hc='arn:aws:route53:::healthcheck/'+each_item['Id']
            np_sers_ids.append(arn_hc)
    
    #Error occur need to check while adding tag
    paginator = route53_con_cli.get_paginator('list_hosted_zones')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['HostedZones']:
            #arn:aws:route53:::hostedzone/Z2QHAIQ3Q2ODS5
            hz_arn = 'arn:aws:route53:::' + each_item['Id'][1:]
            np_sers_ids.append(hz_arn)

##################################################################################################################################################

    SecretsManager_con_cli = boto3.client(service_name='secretsmanager', region_name=each_region)
    paginator = SecretsManager_con_cli.get_paginator('list_secrets')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['SecretList']:
            np_sers_ids.append(each_item['ARN'])

##################################################################################################################################################

    SNS_con_cli = boto3.client(service_name='sns', region_name=each_region)
    paginator = SNS_con_cli.get_paginator('list_topics')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Topics']:
            np_sers_ids.append(each_item['TopicArn'])

##################################################################################################################################################

    ssm_con_cli = boto3.client(service_name='ssm', region_name=each_region)

    # logic to get WindowIdentities
    paginator = ssm_con_cli.get_paginator('describe_maintenance_windows')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['WindowIdentities']:
            #arn:aws:ssm:ap-southeast-1:274138180186:maintenancewindow/mw-043ac0fc5ccac784f
            mw_arn = 'arn:aws:ssm:' + each_region + ':' + account_id + ':maintenancewindow/' + each_item['WindowId']
            np_sers_ids.append(mw_arn)
    
    # logic to get describe_parameters
    paginator = ssm_con_cli.get_paginator('describe_parameters')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Parameters']:
            #arn:aws:ssm:us-east-1:274138180186:parameter/CFN-ADPassword-RaW3KZCsUoag
            pm_arn = 'arn:aws:ssm:' + each_region + ':' + account_id + ':parameter/' + each_item['Name']
            np_sers_ids.append(pm_arn)
    
    # logic to get BaselineIdentities
    paginator = ssm_con_cli.get_paginator('describe_patch_baselines')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['BaselineIdentities']:
            #arn:aws:ssm:us-east-1:274138180186:parameter/CFN-ADPassword-RaW3KZCsUoag
            pb_arn = 'arn:aws:ssm:' + each_region + ':' + account_id + ':patchbaseline/' + each_item['BaselineId']
            np_sers_ids.append(pb_arn)

##################################################################################################################################################

    stepfunctions_con_cli = boto3.client(service_name='stepfunctions', region_name=each_region)
    #logic to get stateMachineArn
    paginator = stepfunctions_con_cli.get_paginator('list_state_machines')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['stateMachines']:
            np_sers_ids.append(each_item['stateMachineArn'])
            
#############################################################################################################


    sqs_con_cli = boto3.client(service_name='sqs', region_name=each_region)
    sqs_url_list =[]
    paginator = sqs_con_cli.get_paginator('list_queues')
    try:
     for each_paginat in paginator.paginate():
         for each_item in each_paginat['QueueUrls']:
             sqs_url_list.append(each_item)

     for each_sqs_url in sqs_url_list:
         txt = each_sqs_url[::-1]
         ind =""
         for eachchar in txt:
             if (eachchar == "/"):
                break
             ind = ind + eachchar
         sqs_arn = 'arn:aws:sqs:' + each_region + ':' + account_id + ':' + ind[::-1]       
         np_sers_ids.append(sqs_arn)
    except:
        print("")
######################################################################################################
##############'###################################################################################################################################

    transfer_con_cli = boto3.client(service_name='transfer', region_name=each_region)
    paginator = transfer_con_cli.get_paginator('list_servers')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Servers']:
            np_sers_ids.append(each_item['Arn'])

##################################################################################################################################################
    wafv2_con_cli = boto3.client(service_name='wafv2', region_name=each_region)

    # logic to get WebACLs
    try:
        for each in wafv2_con_cli.list_web_acls( Scope='CLOUDFRONT',)['WebACLs']:
            np_sers_ids.append(each['ARN'])
    except:
        print("")

    try:
        for each in wafv2_con_cli.list_web_acls( Scope='REGIONAL',)['WebACLs']:
            np_sers_ids.append(each['ARN'])
    except:
        print("")

    try:
        for each in wafv2_con_cli.list_ip_sets( Scope='REGIONAL',)['IPSets']:
            np_sers_ids.append(each['ARN']) 
    except:
        print("")
 
    try:
        for each in wafv2_con_cli.list_ip_sets( Scope='CLOUDFRONT',)['IPSets']:
            np_sers_ids.append(each['ARN'])   
    except:
        print("")

################################################################################################################
#####################################################################################################################
 #Region_ID = ['ap-southeast-1','us-east-1','us-west-2','us-west-2','eu-central-1','eu-west-1']
 #Region_ID  = ['us-west-2']                ***** Need to check***

    appstream_con_cli = boto3.client(service_name="appstream", region_name=each_region)
    
    #logic to get Image ARN
    paginator = appstream_con_cli.get_paginator('describe_images')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['Images']:
             np_sers_ids.append(each_item['Arn'])
    
    # logic for apply tag on describe_stacks
    paginator = appstream_con_cli.get_paginator('describe_stacks')
    for each_paginat in paginator.paginate():
         for each_item in each_paginat['Stacks']:
             np_sers_ids.append(each_item['Arn'])
    
    # logic for apply tag on describe_fleets
    paginator = appstream_con_cli.get_paginator('describe_fleets')
    for each_paginat in paginator.paginate():
         for each_item in each_paginat['Fleets']:
             np_sers_ids.append(each_item['Arn'])
    
    # logic for apply tag on describe_image_builders    
    paginator = appstream_con_cli.get_paginator('describe_image_builders')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['ImageBuilders']:
            np_sers_ids.append(each_item['Arn'])

##################################################################################################################################################

    route53_con_cli = boto3.client(service_name='route53', region_name=each_region)
    paginator = route53_con_cli.get_paginator('list_health_checks')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['HealthChecks']:
            #arn:aws:route53:::healthcheck/a6b887c9-34f3-4935-b844-6a24c404f669
            arn_hc='arn:aws:route53:::healthcheck/'+each_item['Id']
            np_sers_ids.append(arn_hc)

 #Error occur need to check while adding tag
    paginator = route53_con_cli.get_paginator('list_hosted_zones')
    for each_paginat in paginator.paginate():
        for each_item in each_paginat['HostedZones']:
            #arn:aws:route53:::hostedzone/Z2QHAIQ3Q2ODS5
            hz_arn = 'arn:aws:route53:::' + each_item['Id'][1:]
            np_sers_ids.append(hz_arn)

##################################################################################################################################################

    s3_con_cli = boto3.client(service_name='s3', region_name = each_region)
    s3_con_res = boto3.resource('s3', region_name = each_region)
     #logic to list S3 buckets and put tag on the same.
    for each in s3_con_cli.list_buckets()['Buckets']:
      s3_arn= 'arn:aws:s3:::'+ each['Name']
      np_sers_ids.append(s3_arn)
###########################################################################################################
    #logic to list cloudfront_con_cli 
    cloudfront_con_cli = boto3.client('cloudfront')
    distributions=cloudfront_con_cli.list_distributions()
    if distributions['DistributionList']['Quantity'] > 0:
      for distribution in distributions['DistributionList']['Items']:
        np_sers_ids.append(distribution['ARN'])
    
    
    return np_sers_ids