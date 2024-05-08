import os
from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

aws_profile = os.getenv('AWS_PROFILE', 'default') # fallback for default aws configuration if .env was not set

session = boto3.Session(profile_name=aws_profile)
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_resources = request.form.getlist('resource')
        results = {}
        for resource_type in selected_resources:
            if resource_type == 'EC2':
                results['EC2 Instances'] = list_ec2_instances()
            elif resource_type == 'S3':
                results['S3 Buckets'] = list_s3_buckets()
            elif resource_type == 'EKS':
                results['EKS'] = list_eks_clusters()
            elif resource_type == 'VPC':
                results['VPC'] = list_vpcs()
            elif resource_type == 'SG':
                results['SecurityGroup'] = list_security_groups()
            elif resource_type == 'ECR':
                results['ECR'] = list_ecr_repositories()
            elif resource_type == 'RDS':
                results['RDS'] = list_rds_instances()
            elif resource_type == 'RDSSNAP':
                results['RDS Snapshot'] = list_rds_snapshots()
            elif resource_type == 'IAM':
                results['IAM'] = list_iam_users()
            elif resource_type == 'SSM':
                results['SystemsManager'] = list_ssm_parameters()
            elif resource_type == 'SECRETS':
                results['SecretsManager'] = list_secrets()
            elif resource_type == 'LAMBDA':
                results['LAMBDA Functions'] = list_lambda_functions()
            elif resource_type == 'DocumentDB':
                results['DocumentDB Clusters'] = list_documentdb_clusters()
            elif resource_type == 'CloudFront':
                results['CloudFront Distributions'] = list_cloudfront_distributions()
            elif resource_type == 'Route53':
                results['Route 53 Hosted Zones'] = list_route53_hosted_zones()
            elif resource_type == 'APIGateway':
                results['API Gateways'] = list_api_gateways()
            # Add More Resources here
        return render_template('display.html', results=results)
    return render_template('home.html')

#EC2
def list_ec2_instances():
    ec2 = session.client('ec2')
    instances = ec2.describe_instances()
    return [{'id': i['InstanceId'], 'state': i['State']['Name']} for r in instances['Reservations'] for i in r['Instances']]

#S3 Bucket
def list_s3_buckets():
    s3 = session.client('s3')
    buckets = s3.list_buckets()
    return [{'id': bucket['Name'], 'creation_date': bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")} for bucket in buckets['Buckets']]

#EKS
def list_eks_clusters():
    eks = session.client('eks')
    clusters = eks.list_clusters()
    cluster_descriptions = []
    for cluster_name in clusters['clusters']:
        detail = eks.describe_cluster(name=cluster_name)
        cluster_descriptions.append({'name': cluster_name, 'status': detail['cluster']['status']})
    return cluster_descriptions

#VPC
def list_vpcs():
    ec2 = session.client('ec2')
    vpcs = ec2.describe_vpcs()
    return [{'id': vpc['VpcId'], 'state': vpc.get('State', 'N/A')} for vpc in vpcs['Vpcs']]

#Security Groups
def list_security_groups():
    ec2 = session.client('ec2')
    groups = ec2.describe_security_groups()
    return [{'id': group['GroupId'], 'description': group['Description']} for group in groups['SecurityGroups']]

#ECR
def list_ecr_repositories():
    ecr = session.client('ecr')
    repositories = ecr.describe_repositories()
    return [{'name': repo['repositoryName'], 'uri': repo['repositoryUri']} for repo in repositories['repositories']]

#RDS
def list_rds_instances():
    rds = session.client('rds')
    instances = rds.describe_db_instances()
    return [{'id': instance['DBInstanceIdentifier'], 'type': instance['DBInstanceClass']} for instance in instances['DBInstances']]

#RDS Snapshots 
def list_rds_snapshots():
    rds = session.client('rds')
    snapshots = rds.describe_db_snapshots()
    return [{'id': snapshot['DBSnapshotIdentifier'], 'status': snapshot['Status']} for snapshot in snapshots['DBSnapshots']]

#IAM
def list_iam_users():
    iam = session.client('iam')
    users = iam.list_users()
    return [{'id': user['UserName'], 'creation_date': user['CreateDate'].strftime("%Y-%m-%d %H:%M:%S")} for user in users['Users']]

#Systems Manager
def list_ssm_parameters():
    ssm = session.client('ssm')
    parameters = ssm.describe_parameters()
    return [{'name': param['Name'], 'type': param['Type']} for param in parameters['Parameters']]

#Secrets Manager 
def list_secrets():
    secrets_manager = session.client('secretsmanager')
    secrets = secrets_manager.list_secrets()
    return [{'name': secret['Name'], 'last_changed_date': secret['LastChangedDate'].strftime("%Y-%m-%d %H:%M:%S") if 'LastChangedDate' in secret else 'N/A'} for secret in secrets['SecretList']]

#Lambda Functions
def list_lambda_functions():
    lambda_client = session.client('lambda')
    functions = lambda_client.list_functions()
    return [{'name': function['FunctionName'], 'runtime': function['Runtime']} for function in functions['Functions']]

#Amazon DocumentDB
def list_documentdb_clusters():
    rds = session.client('rds')
    clusters = rds.describe_db_clusters()
    # Filtering for DocumentDB clusters
    docdb_clusters = [cluster for cluster in clusters['DBClusters'] if cluster['Engine'] == 'docdb']
    return [{'id': cluster['DBClusterIdentifier'], 'state': cluster['Status']} for cluster in docdb_clusters]

#CloudFront
def list_cloudfront_distributions():
    cloudfront = session.client('cloudfront')
    distributions = cloudfront.list_distributions()
    if 'DistributionList' in distributions and 'Items' in distributions['DistributionList']:
        return [{'id': dist['Id'], 'status': dist['Status'], 'domain_name': dist['DomainName']} for dist in distributions['DistributionList']['Items']]
    return []

#Route 53
def list_route53_hosted_zones():
    route53 = session.client('route53')
    zones = route53.list_hosted_zones()
    return [{'id': zone['Id'], 'name': zone['Name']} for zone in zones['HostedZones']]

#API Gateway
def list_api_gateways():
    apigateway = session.client('apigateway')
    rest_apis = apigateway.get_rest_apis()
    return [{'id': api['id'], 'name': api['name']} for api in rest_apis['items']]

if __name__ == '__main__':
    app.run(debug=True)