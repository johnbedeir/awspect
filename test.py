import boto3

ec2_client = boto3.client('ec2')

# List only enabled regions in your account
response = ec2_client.describe_regions()
enabled_regions = [region['RegionName'] for region in response['Regions']]
print(enabled_regions)
