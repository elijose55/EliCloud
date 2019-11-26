## ARQUITECTURE DIAGRAM
![Hybrid_Cloud.jpg](https://github.com/elijose55/EliCloud/blob/master/images/Hybrid%20Cloud.jpg)

## NETWORK DIAGRAM
![network_diagram.jpg](https://github.com/elijose55/EliCloud/blob/master/images/Network%20Diagram%20(1).jpg)

## You should have the following before getting started:
- Two kubernetes clusters in separate clouds (ex. AWS, GCE).
- Controller access to both clusters.
- IAM permissions to manage and create Instances, LoadBalancers and Persistent Storage in both Cloud Providers.

For the architecture created in this project AWS was used for the public cloud cluster and Openstack for the private cloud cluster.
To create a Kubernetes cluster on the AWS side, an EC2 instance was created using the [create_instance.py](https://github.com/elijose55/EliCloud/blob/master/misc/create_instance.py) program, but it can be done manually in the EC2 dashboard. A simple *t2.micro* instance was created with a Security Group that opens port 22 (SSH connection). Then I used SSH to connect to this instance and created the Kubernetes cluster using [JUJU](https://jaas.ai/docs/installing). I noted the commands used in this deploy and they are available in [K8s_juju_deploy_instructions](https://github.com/elijose55/EliCloud/blob/master/misc/create_instance.py).

For the private cloud Kubernetes deploy, it was much more complicated and lenghty as I used MAAS and JUJU to create the Openstack infrastructure on top of my physical machines, and on top of that I deployed the Kubernetes cluster. For that reason I did not upload any material for it as it would be incomplete and inaccurate, but if you are interested contact me: [elijose55@hotmail.com](mailto:elijose55@hotmail.com).

### PRIVATE CLOUD STACK DIAGRAM







## PRE-REQUIREMENTS
- `sudo apt-get install kubectl`


## DEPLOYMENT SCRIPT CONFIGURATION
To run the deployment script just replace the shown values bellow with the public IPs of AWS instance from where you control the Kubernetes cluster and with the IP of the MAAS instance in the [EliCloud](https://github.com/elijose55/EliCloud/blob/master/EliCloud) file:

```
rm eli.ovpn
rsync -I scripts/aws_script ubuntu@[AWS_INSTANCE_PUBLIC_IP]:~/
cat scripts/aws_script | ssh ubuntu@[AWS_INSTANCE_PUBLIC_IP]
sftp ubuntu@[AWS_INSTANCE_PUBLIC_IP]:EliCloud/openvpn/eli.ovpn .
sshpass -p "cloudp" rsync -I eli.ovpn cloud@[MAAS_INSTANCE_PUBLIC_IP]:~/
sshpass -p "cloudp" rsync -I scripts/openstack_script cloud@[MAAS_INSTANCE_IP]:~/
sshpass -p "cloudp" rsync -I scripts/maas_script cloud@[MAAS_INSTANCE_IP]:~/
cat scripts/maas_script | sshpass -p "cloudp" ssh cloud@[MAAS_INSTANCE_IP]
echo FINISH
```
Then do the same for the [maas_script](https://github.com/elijose55/EliCloud/blob/master/scripts/maas_script) file, but replace the shown values bellow with the Openstack instance IP from where you can control the Kubernetes cluster:

``` 
rsync -I eli.ovpn ubuntu@[OPENSTACK_INSTANCE_IP]:~/
rm eli.ovpn
chmod +x openstack_script
cat openstack_script | ssh ubuntu@[OPENSTACK_INSTANCE_IP]
exit
```


## RUNNING THE SCRIPT

To use the script and build the whole infrastructure just make the EliCloud script executable and run it.

`` 
chmod +x EliCloud
``

``
./EliCloud
``


