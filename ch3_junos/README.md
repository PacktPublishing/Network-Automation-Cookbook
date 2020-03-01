The Repo Inlucde all the Ansible playbooks and Roles which outlines how to interact with Juniper Devices using Ansible as outlined in CH03 of the Network Automation Cookbook.

All Our network topology and network design is mainly defined under the `group_vars/all.yml`


Below are the main playbooks and tasks implemented

### 1. Enable NETCONF 

Run the playbook `pb_jnpr_net_build.yml` with the *`netconf`* tag as shown below

```
ansible-playbook pb_jnpr_net_build.yml --tag netconf
```

### 2. Basic Device Configuration

In order to setup the basic system parameters like Uses and DNS run the playbook as shown below

``` 
ansible-playbook pb_jnpr_basic_config.yml --tags system 
```

In order to setup Interfaces run the playbook as shown below

``` 
ansible-playbook pb_jnpr_basic_config.yml --tags intf 
```


### 3. Build Network Configuration


In order to generate the configuration for Our Demo Network which includes the configuration for the following
- Interfaces
- OSPF
- MPLS
- BGP


We run the following playbook as shown below

``` 
ansible-playbook pb_jnpr_net_build.yml --tags build
```

All the configuration for all the devices will be generated on the ##configs directory

We push the generated configuration onto the devices as shown below

``` 
ansible-playbook pb_jnpr_net_build.yml --tags deploy
```

### 4. Validate Network Setup

We can use multiple playbooks to validate Network State as shown below

- We can validate the Physical interface status and build basic System reports using `junos_facts` module as shown below

```
ansible-playbook pb_jnpr_facts.yml
```

- We can Validate OSPF peering status using `junos_command` and `assert` module as shown below 

```
ansible-playbook pb_get_ospf_peers.yml
```

- We can validate BGP Status using JunOS PyeZ Tables as shown below

```
ansible-playbook pb_jnpr_pyez_table.yml --diff
```

- We Can validate Network Reachability using `junos_ping` as shown below

```
ansible-playbook pb_junos_ping.yml
```

### 5. Deploy L3VPN 

We define our L3VPN setup in the **l3vpn.yml** file and we can deploy L3VPN using `junos_l3vpn` with the below playbook

```
ansible-playbook pb_junos_l3vpn.yml
```