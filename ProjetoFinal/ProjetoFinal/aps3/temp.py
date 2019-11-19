import boto3
from botocore.exceptions import ClientError
import botocore
import paramiko

ec2 = boto3.client('ec2')



key_name = "projetoEli"

security_group_name = "projetoEli"

instance_name = "EliCloud"
instance_type = "t2.micro"
image_id = "ami-0a309f3b728183374"
number_of_instances = 1

instance_ip = "3.95.188.103"

key = paramiko.RSAKey.from_private_key_file("~/.ssh/id_rsa.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:

	# Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

	client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

	# Execute a command(cmd) after connecting/ssh to an instance

	stdin, stdout, stderr = client.exec_command("git clone https://github.com/elijose55/CloudComputing.git")

	print (stdout.read())

	# close the client connection once the job is done

	client.close()

except Exception as e:

	print(e)

