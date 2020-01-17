ansible-pyats
=========

ansible-genie is a implementation of the [pyATS](https://developer.cisco.com/pyats/) network testing framework in an
Ansible role.  It contains modules, filters, and tasks:
* Run a command and get structured output
* "snapshot" the output of a command and save it to a file
* Compare the current output of a command to a previous "snapshot"

## Installation

First, install the Python dependencies:

```bash
$ pip install pyats genie
<snip>
Installing collected packages: pyats, genie
Successfully installed genie-19.9 pyats-19.9.2
```

> pyATS and Genie require Python >=3.4.

### Manual

For manual installation, you can just clone the repository into your
[`ANSIBLE_ROLES_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-roles-path):

```bash
$ git clone https://github.com/CiscoDevNet/ansible-pyats "${ANSIBLE_ROLES_PATH:-roles}/ansible-pyats"
Cloning into 'roles/ansible-pyats'...
remote: Enumerating objects: 83, done.
remote: Counting objects: 100% (83/83), done.
remote: Compressing objects: 100% (56/56), done.
remote: Total 83 (delta 28), reused 56 (delta 12), pack-reused 0
Unpacking objects: 100% (83/83), done.
```


### Ansible Galaxy

If you are using [Ansible Galaxy](https://docs.ansible.com/ansible/latest/reference_appendices/galaxy.html),
you can use this role by adding the following to your `requirements.yml`:

```yaml
- src: https://github.com/CiscoDevNet/ansible-pyats
  scm: git
  name: ansible-pyats
```

Next, install your Galaxy dependencies:

```bash
$ ansible-galaxy install -r requirements.yml -p "${ANSIBLE_ROLES_PATH:-roles}"
```

## Modules
* `pyats_parse_command`: Run a command on a remote device and return the structured output

## Filters
* `pyats_parser`: provides structured data from unstructured command output
* `pyats_diff`: provides the difference between two data structures

## Example Playbooks

### Run a command and retrieve the structured output
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - pyats_parse_command:
        command: show ip route bgp
      register: output

    - debug:
        var: output.structured
```

### Snapshot the output of a command to a file
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - include_role:
        name: ansible-pyats
        tasks_from: snapshot_command
      vars:
        command: show ip route
        file: "{{ inventory_hostname }}_routes.json"
```

#### Role Variables

* `command`: the command to run on the device
* `file`: the name of the file in which to store the command "shapshot"

### Compare the output of a command with a previous snapshot
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - include_role:
        name: ansible-pyats
        tasks_from: compare_command
      vars:
        command: show ip route
        file: "{{ inventory_hostname }}_routes.json"
```

#### Role Variables

* `command`: the command to run on the device
* `file`: the name of the file in which to store the command "shapshot"

### Using the `pyats_parser` filter directly
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - name: Run command
      cli_command:
        command: show ip route
      register: cli_output
    
    - name: Parsing output
      set_fact:
        parsed_output: "{{ cli_output.stdout | pyats_parser('show ip route', 'iosxe') }}"
```

### Using the `pyats_diff` filter directly
```yaml
- name: Diff current and snapshot
  set_fact:
    diff_output: "{{ current_output | pyats_diff(previous_output) }}"
```

### Change ACL configuration and compare before and after configs using `genie_config_diff`
```yaml
---

- hosts: cisco
  gather_facts: no
  connection: network_cli

  tasks:
    - name: collect config (before)
      ios_command:
        commands:
          - show run
      register: result_before

    - name: load new acl into device
      ios_config:
        lines:
          - permit ip host 192.168.114.1 any
          - permit ip host 192.168.114.2 any
          - permit ip host 192.168.114.3 any
        parents: ip access-list extended test
        save_when: modified

    - name: collect config (after)
      ios_command:
        commands:
          - show run
      register: result_after

    - name: debug
      debug:
        msg: "{{ result_before.stdout[0] | genie_config_diff(result_after.stdout[0], mode='add', exclude=exclude_list) }}"

  vars:
    exclude_list:
      - (^Using.*)
      - (Building.*)
      - (Current.*)
      - (crypto pki certificate chain.*)
```
The argument `mode` can be `add` (displays added commands in result_after), `remove` (displays removed commands in result_after), or `modified` (displays modified commands). If `mode` argument is not specified, added, removed, and modified commands are displayed.  
The argument `exclude` means command lists which is excluded when comparing before and after configs.
In the playbook example above, variable `excluded_list`, which is defined as the play variable, is used.

#### Other examples
```yaml
        msg: "{{ result_before.stdout[0] | genie_config_diff(result_after.stdout[0]) }}"
        msg: "{{ result_before.stdout[0] | genie_config_diff(result_after.stdout[0], mode='remove') }}"
        msg: "{{ result_before.stdout[0] | genie_config_diff(result_after.stdout[0], exclude=exclude_list) }}"
```

#### The result of example playbook
```yaml
PLAY [cisco] **********************************************************************************

TASK [collect config (before)] ****************************************************************
ok: [test3]

TASK [load new acl into device] ***************************************************************
ok: [test3]

TASK [collect config (after)] *****************************************************************
ok: [test3]

TASK [debug] **********************************************************************************
ok: [test3] => {
    "msg": [
        "ip access-list extended test:",
        "+ permit ip host 192.168.114.1 any: ",
        "+ permit ip host 192.168.114.2 any: ",
        "+ permit ip host 192.168.114.3 any: "
    ]
}

PLAY RECAP ************************************************************************************
test3                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```


### Compare show commands using `genie_parser_diff`
This filter can compare the output of show commands parsed by Genie parser. The arguments `mode` and `exclude` also can be used.

```yaml
    - name: debug
      debug:
        msg: "{{ sh_int_parsed_before | genie_parser_diff(sh_int_parsed_after, mode='modified', exclude=exclude_list) }}"
        
  vars:
    exclude_list:
      - (.*in_octets.*)
      - (.*in_pkts.*)
      - (.*out_octets.*)
      - (.*out_pkts.*)
```

License
-------

Cisco Sample License

