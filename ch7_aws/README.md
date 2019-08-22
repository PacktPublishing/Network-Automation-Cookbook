# AWS Networking Build with Ansible

This repo containes all playbooks to build AWS VPCs across multiple regions and configure all the different components like VPC subnets and IGWs.

In order to utilize these playbooks to provision the VPCs resources you need to use your own aws account credentials and update the aws_access_key and aws_secret_key_id in all.yml file.

In order to provision the VPCs run the following playbook
##### ansible-playbook pb_vpc_build.yml



In order to delete all the VPCs and all the other components run the following playbook
#### ansible-playbook pb_delete_vpc.yml
