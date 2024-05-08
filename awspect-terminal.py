import boto3

session = boto3.Session(profile_name='default')

#EC2
def list_ec2_instances():
    ec2 = session.client('ec2')
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"EC2 Instance ID: {instance['InstanceId']} - State: {instance['State']['Name']}")

#S3 Bucket
def list_s3_buckets():
    s3 = session.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f"S3 Bucket: {bucket['Name']}")

#EKS
def list_eks_clusters():
    eks = session.client('eks')
    clusters = eks.list_clusters()
    for cluster in clusters['clusters']:
        print(f"EKS Cluster: {cluster}")

#VPC
def list_vpcs():
    ec2 = session.client('ec2')
    vpcs = ec2.describe_vpcs()
    for vpc in vpcs['Vpcs']:
        print(f"VPC ID: {vpc['VpcId']} - State: {vpc['State']}")

#Security Groups
def list_security_groups():
    ec2 = session.client('ec2')
    groups = ec2.describe_security_groups()
    for group in groups['SecurityGroups']:
        print(f"Security Group: {group['GroupId']} - Description: {group['Description']}")

#ECR
def list_ecr_repositories():
    ecr = session.client('ecr')
    repositories = ecr.describe_repositories()
    for repo in repositories['repositories']:
        print(f"ECR Repository: {repo['repositoryName']}")

#RDS
def list_rds_instances():
    rds = session.client('rds')
    instances = rds.describe_db_instances()
    for instance in instances['DBInstances']:
        print(f"RDS Instance: {instance['DBInstanceIdentifier']}")

#RDS Snapshots 
def list_rds_snapshots():
    rds = session.client('rds')
    snapshots = rds.describe_db_snapshots()
    for snapshot in snapshots['DBSnapshots']:
        print(f"RDS Snapshot: {snapshot['DBSnapshotIdentifier']}")

#IAM
def list_iam_users():
    iam = session.client('iam')
    users = iam.list_users()
    for user in users['Users']:
        print(f"IAM User: {user['UserName']}")

#Systems Manager
def list_ssm_parameters():
    ssm = session.client('ssm')
    params = ssm.describe_parameters()
    for param in params['Parameters']:
        print(f"SSM Parameter: {param['Name']}")

#Secrets Manager 
def list_secrets():
    secrets_manager = session.client('secretsmanager')
    secrets = secrets_manager.list_secrets()
    for secret in secrets['SecretList']:
        print(f"Secret: {secret['Name']}")

#Lambda Functions
def list_lambda_functions():
    lambda_client = session.client('lambda')
    functions = lambda_client.list_functions()
    for function in functions['Functions']:
        print(f"Lambda Function: {function['FunctionName']}")

#Amazon DocumentDB
def list_documentdb_clusters():
    rds = session.client('rds')
    clusters = rds.describe_db_clusters()
    for cluster in clusters['DBClusters']:
        if cluster['Engine'] == 'docdb':
            print(f"DocumentDB Cluster ID: {cluster['DBClusterIdentifier']} - State: {cluster['Status']}")

#CloudFront
def list_cloudfront_distributions():
    cloudfront = session.client('cloudfront')
    distributions = cloudfront.list_distributions()
    if 'DistributionList' in distributions and 'Items' in distributions['DistributionList']:
        for dist in distributions['DistributionList']['Items']:
            print(f"CloudFront Distribution ID: {dist['Id']} - Status: {dist['Status']} - Domain: {dist['DomainName']}")

#Route 53
def list_route53_hosted_zones():
    route53 = session.client('route53')
    zones = route53.list_hosted_zones()
    for zone in zones['HostedZones']:
        print(f"Route 53 Hosted Zone ID: {zone['Id']} - Name: {zone['Name']}")

#API Gateway
def list_api_gateways():
    apigateway = session.client('apigateway')
    rest_apis = apigateway.get_rest_apis()
    for api in rest_apis['items']:
        print(f"API Gateway ID: {api['id']} - Name: {api['name']}")

if __name__ == "__main__":
    print("Listing EC2 Instances:")
    list_ec2_instances()
    print("\nListing S3 Buckets:")
    list_s3_buckets()
    print("\nListing EKS Clusters:")
    list_eks_clusters()
    print("\nListing VPCs:")
    list_vpcs()
    print("\nListing Security Groups:")
    list_security_groups()
    print("\nListing ECR Repositories:")
    list_ecr_repositories()
    print("\nListing RDS Instances:")
    list_rds_instances()
    print("\nListing RDS Snapshots:")
    list_rds_snapshots()
    print("\nListing IAM Users:")
    list_iam_users()
    print("\nListing Systems Manager Parameters:")
    list_ssm_parameters()
    print("\nListing Secrets Manager Secrets:")
    list_secrets()
    print("\nListing Lambda Functions:")
    list_lambda_functions()
    print("Listing DocumentDB Clusters:")
    list_documentdb_clusters()
    print("Listing CloudFront Distributions:")
    list_cloudfront_distributions()
    print("Listing Route 53 Hosted Zones:")
    list_route53_hosted_zones()
    print("Listing API Gateways:")
    list_api_gateways()