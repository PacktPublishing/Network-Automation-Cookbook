import yaml
import os
import re

SERVICE_VLANS = 3

def test_read_files():
    wan_data = yaml.load(open('group_vars/wan.yml',mode='r'))
    print(type(wan_data))
    assert isinstance(wan_data,dict)

def test_all_vlan_is_valid():
    lan_data= yaml.load(open('group_vars/lan.yaml',mode='r'))
    vlans = [x['vlan_id'] for x in lan_data['vlans'] if 0 < x['vlan_id'] < 4096 ]
    assert len(vlans) == SERVICE_VLANS
    assert svi_vlans == vlans

def test_all_svi_are_valid():
    core_data= yaml.load(open('group_vars/core.yml',mode='r'))
    svi = [ x['name'] for x in core_data['svi_interfaces'] if x['vrrp'] == True ]
    assert len(svi) == SERVICE_VLANS
    svi_vlans = [ int(x.split('Vlan')[1]) for x in svi if 0 < int(x.split('Vlan')[1]) < 4096 ]
    assert len(svi_vlans) == SERVICE_VLANS



test_read_files()
