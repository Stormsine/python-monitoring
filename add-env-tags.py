import boto3

ec2_client_ohio = boto3.client('ec2', region_name="us-east-2")
ec2_resource_ohio = boto3.resource('ec2', region_name="us-east-2")

ec2_client_n_virginia = boto3.client('ec2', region_name="us-east-1")
ec2_resource_n_virginia = boto3.resource('ec2', region_name="us-east-1")

instances_ids_ohio = []
instances_ids_n_virginia = []

reservations_ohio = ec2_client_ohio.describe_instances()['Reservations']
for res in reservations_ohio:
    instances = res['Instances']
    for ins in instances:
        instances_ids_ohio.append(ins['InstanceId'])

response = ec2_resource_ohio.create_tags(
    Resources=instances_ids_ohio,
    Tags=[
        {
            'Key': 'string',
            'Value': 'environmental'
        },
    ]
)

reservations_n_virginia = ec2_client_n_virginia.describe_instances()['Reservations']
for res in reservations_n_virginia:
    instances = res['Instances']
    for ins in instances:
        instances_ids_n_virginia.append(ins['InstanceId'])

response = ec2_resource_n_virginia.create_tags(
    Resources=instances_ids_n_virginia,
    Tags=[
        {
            'Key': 'string',
            'Value': 'dev'
        },
    ]
)
