import os
from flask import Flask, render_template, request
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Create a session for global AWS services (S3, IAM, CloudFront, Route53, APIGateway)
session = boto3.Session()

ec2_client = boto3.client('ec2')

# List only enabled regions in your account
response = ec2_client.describe_regions()
enabled_regions = [region['RegionName'] for region in response['Regions']]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_resources = request.form.getlist('resource')
        selected_regions = request.form.getlist('regions')

        # Handle 'All Regions' selection
        if 'all' in selected_regions:
            selected_regions = enabled_regions

        results = {}

        for resource_type in selected_resources:
            try:
                if resource_type == 'EC2':
                    results['EC2 Instances'] = list_ec2_instances(selected_regions)
                elif resource_type == 'S3':
                    results['S3 Buckets'] = list_s3_buckets()
                elif resource_type == 'EKS':
                    results['EKS'] = list_eks_clusters(selected_regions)
                elif resource_type == 'VPC':
                    results['VPC'] = list_vpcs(selected_regions)
                elif resource_type == 'SG':
                    results['SecurityGroup'] = list_security_groups(selected_regions)
                elif resource_type == 'ECR':
                    results['ECR'] = list_ecr_repositories(selected_regions)
                elif resource_type == 'RDS':
                    results['RDS'] = list_rds_instances(selected_regions)
                elif resource_type == 'RDSSNAP':
                    results['RDS Snapshot'] = list_rds_snapshots(selected_regions)
                elif resource_type == 'IAM':
                    results['IAM'] = list_iam_users()
                elif resource_type == 'SSM':
                    results['SystemsManager'] = list_ssm_parameters(selected_regions)
                elif resource_type == 'SECRETS':
                    results['SecretsManager'] = list_secrets(selected_regions)
                elif resource_type == 'LAMBDA':
                    results['LAMBDA Functions'] = list_lambda_functions(selected_regions)
                elif resource_type == 'DocumentDB':
                    results['DocumentDB Clusters'] = list_documentdb_clusters(selected_regions)
                elif resource_type == 'CloudFront':
                    results['CloudFront Distributions'] = list_cloudfront_distributions()
                elif resource_type == 'Route53':
                    results['Route 53 Hosted Zones'] = list_route53_hosted_zones()
                elif resource_type == 'APIGateway':
                    results['API Gateways'] = list_api_gateways(selected_regions)
            except ClientError as e:
                results[resource_type] = {
                    "error": e.response["Error"]["Message"]
                }

        return render_template('display.html', results=results)

    return render_template('home.html', regions=enabled_regions)

# EC2 - Modified to support regions
def list_ec2_instances(regions):
    all_instances = []
    for region in regions:
        try:
            ec2 = boto3.client('ec2', region_name=region)
            instances = ec2.describe_instances()
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    all_instances.append({
                        'region': region,
                        'id': instance['InstanceId'],
                        'state': instance['State']['Name']
                    })
        except ClientError as e:
            all_instances.append({
                'region': region,
                'error': str(e)
            })
    return all_instances

# S3 Bucket - Global service (no region needed)
def list_s3_buckets():
    s3 = session.client('s3')
    buckets = s3.list_buckets()
    return [{'id': bucket['Name'], 'creation_date': bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")} for bucket in buckets['Buckets']]

# EKS - Modified to support regions
def list_eks_clusters(regions):
    all_clusters = []
    for region in regions:
        try:
            eks = boto3.client('eks', region_name=region)
            clusters = eks.list_clusters()
            for cluster_name in clusters['clusters']:
                detail = eks.describe_cluster(name=cluster_name)
                all_clusters.append({
                    'region': region,
                    'name': cluster_name,
                    'status': detail['cluster']['status']
                })
        except ClientError as e:
            all_clusters.append({
                'region': region,
                'error': str(e)
            })
    return all_clusters

# VPC - Modified to support regions
def list_vpcs(regions):
    all_vpcs = []
    for region in regions:
        try:
            ec2 = boto3.client('ec2', region_name=region)
            vpcs = ec2.describe_vpcs()
            for vpc in vpcs['Vpcs']:
                all_vpcs.append({
                    'region': region,
                    'id': vpc['VpcId'],
                    'state': vpc.get('State', 'N/A')
                })
        except ClientError as e:
            all_vpcs.append({
                'region': region,
                'error': str(e)
            })
    return all_vpcs

# Security Groups - Modified to support regions
def list_security_groups(regions):
    all_groups = []
    for region in regions:
        try:
            ec2 = boto3.client('ec2', region_name=region)
            groups = ec2.describe_security_groups()
            for group in groups['SecurityGroups']:
                all_groups.append({
                    'region': region,
                    'id': group['GroupId'],
                    'description': group['Description']
                })
        except ClientError as e:
            all_groups.append({
                'region': region,
                'error': str(e)
            })
    return all_groups

# ECR - Modified to support regions
def list_ecr_repositories(regions):
    all_repos = []
    for region in regions:
        try:
            ecr = boto3.client('ecr', region_name=region)
            repositories = ecr.describe_repositories()
            for repo in repositories['repositories']:
                all_repos.append({
                    'region': region,
                    'name': repo['repositoryName'],
                    'uri': repo['repositoryUri']
                })
        except ClientError as e:
            all_repos.append({
                'region': region,
                'error': str(e)
            })
    return all_repos

# RDS - Modified to support regions
def list_rds_instances(regions):
    all_instances = []
    for region in regions:
        try:
            rds = boto3.client('rds', region_name=region)
            instances = rds.describe_db_instances()
            for instance in instances['DBInstances']:
                all_instances.append({
                    'region': region,
                    'id': instance['DBInstanceIdentifier'],
                    'type': instance['DBInstanceClass']
                })
        except ClientError as e:
            all_instances.append({
                'region': region,
                'error': str(e)
            })
    return all_instances

# RDS Snapshots - Modified to support regions
def list_rds_snapshots(regions):
    all_snapshots = []
    for region in regions:
        try:
            rds = boto3.client('rds', region_name=region)
            snapshots = rds.describe_db_snapshots()
            for snapshot in snapshots['DBSnapshots']:
                all_snapshots.append({
                    'region': region,
                    'id': snapshot['DBSnapshotIdentifier'],
                    'status': snapshot['Status']
                })
        except ClientError as e:
            all_snapshots.append({
                'region': region,
                'error': str(e)
            })
    return all_snapshots

# IAM - Global service (no region needed)
def list_iam_users():
    iam = session.client('iam')
    users = iam.list_users()
    return [{'id': user['UserName'], 'creation_date': user['CreateDate'].strftime("%Y-%m-%d %H:%M:%S")} for user in users['Users']]

# Systems Manager - Modified to support regions
def list_ssm_parameters(regions):
    all_params = []
    for region in regions:
        try:
            ssm = boto3.client('ssm', region_name=region)
            parameters = ssm.describe_parameters()
            for param in parameters['Parameters']:
                all_params.append({
                    'region': region,
                    'name': param['Name'],
                    'type': param['Type']
                })
        except ClientError as e:
            all_params.append({
                'region': region,
                'error': str(e)
            })
    return all_params

# Secrets Manager - Modified to support regions
def list_secrets(regions):
    all_secrets = []
    for region in regions:
        try:
            secrets_manager = boto3.client('secretsmanager', region_name=region)
            secrets = secrets_manager.list_secrets()
            for secret in secrets['SecretList']:
                all_secrets.append({
                    'region': region,
                    'name': secret['Name'],
                    'last_changed_date': secret['LastChangedDate'].strftime("%Y-%m-%d %H:%M:%S") if 'LastChangedDate' in secret else 'N/A'
                })
        except ClientError as e:
            all_secrets.append({
                'region': region,
                'error': str(e)
            })
    return all_secrets

# Lambda Functions - Modified to support regions
def list_lambda_functions(regions):
    all_functions = []
    for region in regions:
        try:
            lambda_client = boto3.client('lambda', region_name=region)
            functions = lambda_client.list_functions()
            for function in functions['Functions']:
                all_functions.append({
                    'region': region,
                    'name': function['FunctionName'],
                    'runtime': function['Runtime']
                })
        except ClientError as e:
            all_functions.append({
                'region': region,
                'error': str(e)
            })
    return all_functions

# Amazon DocumentDB - Modified to support regions
def list_documentdb_clusters(regions):
    all_clusters = []
    for region in regions:
        try:
            rds = boto3.client('rds', region_name=region)
            clusters = rds.describe_db_clusters()
            # Filtering for DocumentDB clusters
            docdb_clusters = [cluster for cluster in clusters['DBClusters'] if cluster['Engine'] == 'docdb']
            for cluster in docdb_clusters:
                all_clusters.append({
                    'region': region,
                    'id': cluster['DBClusterIdentifier'],
                    'state': cluster['Status']
                })
        except ClientError as e:
            all_clusters.append({
                'region': region,
                'error': str(e)
            })
    return all_clusters

# CloudFront - Global service (no region needed)
def list_cloudfront_distributions():
    cloudfront = session.client('cloudfront')
    distributions = cloudfront.list_distributions()
    if 'DistributionList' in distributions and 'Items' in distributions['DistributionList']:
        return [{'id': dist['Id'], 'status': dist['Status'], 'domain_name': dist['DomainName']} for dist in distributions['DistributionList']['Items']]
    return []

# Route 53 - Global service (no region needed)
def list_route53_hosted_zones():
    route53 = session.client('route53')
    zones = route53.list_hosted_zones()
    return [{'id': zone['Id'], 'name': zone['Name']} for zone in zones['HostedZones']]

# API Gateway - Modified to support regions
def list_api_gateways(regions):
    all_apis = []
    for region in regions:
        try:
            apigateway = boto3.client('apigateway', region_name=region)
            rest_apis = apigateway.get_rest_apis()
            for api in rest_apis['items']:
                all_apis.append({
                    'region': region,
                    'id': api['id'],
                    'name': api['name']
                })
        except ClientError as e:
            all_apis.append({
                'region': region,
                'error': str(e)
            })
    return all_apis

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)