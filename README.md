## ARQUITECTURE DIAGRAM
![Hybrid_Cloud.jpg](https://github.com/elijose55/EliCloud/blob/master/images/Hybrid%20Cloud.jpg)

## You should have the following before getting started:
- Two kubernetes clusters in separate clouds (ex. AWS, GCE).
- Controller access to both clusters.
- IAM permissions to manage and create Instances, LoadBalancers and Persistent Storage in both Cloud Providers.

For the architecture created in this project AWS was used for the public cloud cluster and Openstack for the private cloud cluster.
To create a Kubernetes cluster on the AWS side, an EC2 instance was created using the [create_instance.py](https://github.com/elijose55/EliCloud/blob/master/misc/create_instance.py) program, but it can be done manually in the EC2 dashboard. A simple *t2.micro* instance was created with a Security Group that opens port 22 (SSH connection). Then I used SSH to connect to this instance and created the Kubernetes cluster using [JUJU](https://jaas.ai/docs/installing). I noted the commands used in this deploy and they are available in [K8s_juju_deploy_instructions](https://github.com/elijose55/EliCloud/blob/master/misc/create_instance.py).

For the private cloud Kubernetes deploy, it was much more complicated and lenghty as I used MAAS and JUJU to create the Openstack infrastructure on top of my physical machines, and on top of that I deployed the Kubernetes cluster. For that reason I did not upload any material for it as it would be incomplete and inaccurate, but if you are interested contact me: [elijose55@hotmail.com](mailto:elijose55@hotmail.com).

### PRIVATE CLOUD STACK DIAGRAM
![alt text](https://github.com/elijose55/EliCloud/blob/master/images/Hybrid%20Cloud.jpg)



## PRE-REQUIREMENTS
- `sudo apt-get install kubectl`

## DEPLOYMENT SCRIPT

