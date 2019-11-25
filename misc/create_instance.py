import boto3
from botocore.exceptions import ClientError
import botocore
import paramiko

ec2 = boto3.client('ec2')


######



def keyPairConfig(key_name):
	response = ec2.describe_key_pairs()

	for i in response["KeyPairs"]:
		if (i["KeyName"] == key_name):
			print("Key Pair '{0}' found! Deleting key..." .format(key_name))
			ec2.delete_key_pair(KeyName=key_name)


	response = ec2.import_key_pair(
		KeyName='projetoEli',
		PublicKeyMaterial=b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6mBHm6LPNPdeCAcUZ+bZXgX3+lAsqEyF5XUrEXtaVahrNjqj0/YWCvGu1C1nHLshAAHVNk2lZ8igVI2dfig9SFFDLyg7hAFR0cWc4Ap2Hn0fJlx9dBtv+0R8RYR8w/vnT3THih5bCE37lukK6iswXGsEtEvTolWydhlkU/o3bEsA+gz+vprra8rVzYqLAAO5BcvMDAhmrpLrWSvSM62lZTrjM/aR8Zj5n+Br7grqYUCQ/dVxwQ9/AZhl5D6WkPksxBZnZJnaTx6MKQkdaDJGj0Twd8HS1INtvg7dmt+I/EmmEwUMs4SECY0AuKDLhbNzttApZxwzCZbHmEmK+Qkw3 eli@elijag'
	)
	print("Key '{0}' created." .format(key_name))
	return


def securityGroupConfig(name):

	try:
		response = ec2.describe_security_groups()
		for i in response["SecurityGroups"]:
			if(i["GroupName"] == name):
				print("Security Group '{0}' found! Deleting group..." .format(name))
				ec2.delete_security_group(GroupName=name)
	except ClientError as e:
		print(e)
		return

	#Criar security group
	try:
		response = ec2.describe_vpcs()
		vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

		response = ec2.create_security_group(GroupName=name,Description='Security Group Eli, it opens ports 22 and 5000',VpcId=vpc_id)
		security_group_id = response['GroupId']


		ec2.authorize_security_group_ingress(
		  GroupId=security_group_id,
		  IpPermissions=[
			  {'IpProtocol': 'tcp',
			  'FromPort': 5000,
			  'ToPort': 5000,
			  'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
			  {'IpProtocol': 'tcp',
			  'FromPort': 22,
			  'ToPort': 22,
			  'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
		])
		print("Security Group '{0}' created." .format(name))
		return
	except ClientError as e:
		print(e)
		return

#######


def create_instances(name, image_id, instance_type, key_name, security_group_name, number_of_instances):
	try:
		response = ec2.describe_instances(
		Filters=[
			{
				'Name': 'tag:Name',
				'Values': [
					name,
				]
			},
		]
		)
		if(len(response['Reservations']) > 0):
			print("Instance Name: '{0}' found! Terminating instance..." .format(name))

			instances = response["Reservations"]
			waiter = ec2.get_waiter('instance_terminated')
			for instance in instances:
				#print(instance["Instances"][0]["InstanceId"])
				ec2.terminate_instances(InstanceIds=[instance["Instances"][0]["InstanceId"]], DryRun=False)
				waiter.wait(InstanceIds=[instance["Instances"][0]["InstanceId"]])

		else:
			print("No Instances to terminate...")

		securityGroupConfig(security_group_name)

		print("Creating instance '{0}'..." .format(name))
		response = ec2.run_instances(
		  ImageId=image_id,
		  InstanceType= instance_type,
		  MinCount=number_of_instances,
		  MaxCount=number_of_instances,
		  KeyName=key_name,
		  SecurityGroups=[security_group_name],
		  TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'Owner','Value': 'Eli'}, {'Key': 'Name','Value': 'EliCloud'}]}]
		)
		waiter = ec2.get_waiter('instance_running')
		waiter.wait(InstanceIds=[response["Instances"][0]["InstanceId"]])

		print("Instance created")

		response = ec2.describe_instances(InstanceIds=[response["Instances"][0]["InstanceId"]])
		instance_ip = response["Reservations"][0]["Instances"][0]["PublicIpAddress"]
		print("Instance Public IP is: '{0}'" .format(instance_ip))
		print("Run:  $ ssh ubuntu@{0}" .format(instance_ip))

		return instance_ip

		

	except ClientError as e:
		print(e)
		return





key_name = "projetoEli"

security_group_name = "projetoEli"

instance_name = "EliCloud"
instance_type = "t2.micro"
image_id = "ami-0a309f3b728183374"
number_of_instances = 1

keyPairConfig(key_name)
instance_ip = create_instances(instance_name, image_id, instance_type, key_name, security_group_name, number_of_instances)


