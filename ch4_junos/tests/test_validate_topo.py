import yaml
import pytest

TOPOLOGY_FILE = 'network_topology.yml'
NUM_OF_LINKS = 7

@pytest.fixture()
def net_topo():
    '''
    Read the Network Topololgy YAML File
    '''
    with open(TOPOLOGY_FILE, mode='r') as fin:
        topo = yaml.safe_load(fin)
        return topo

def test_valid_keys(net_topo):
    '''
    Validate that 'fabric' is a Main key
    '''
    assert 'fabric' in net_topo.keys()

def test_num_of_links(net_topo):
    '''
    Validate Correct Number of Interfaces
    '''
    fabric = net_topo['fabric']
    links = list()
    for node in fabric:
        node_links = [ _x['link_id'] for intf,_x in fabric[node].items()]
        links.extend(node_links)
    assert len(set(links)) == NUM_OF_LINKS
    assert max(links) == NUM_OF_LINKS
    

def test_unique_interfaces(net_topo):
    '''
    Validate All Interface are Unique per each Device
    '''
    fabric = net_topo['fabric']
    for node in fabric:
        intfs = fabric[node].keys()
        assert len(intfs) == len(set(intfs))

# def test_matching_link_id(net_topo):
#     '''
#     Validate that the matching link_id appear on each
#     side of the link
#     '''
#     fabric = net_topo['fabric']
#     for node,ports in fabric.items():
#         for port in ports:
#             #print(fabric[node].get(port)['link_id'])
#             link_id = fabric[node][port]['link_id']
#             peer = fabric[node][port]['peer']
#             peer_port = fabric[node][port]['pport']
#             assert fabric[peer].get(peer_port)['link_id'] == range(1,100) ,\
#                      'node:{} has no matching link_id with {} with {}'.format(node,peer,peer_port)
#             peer_link_id = fabric[peer].get(peer_port)['link_id']
#             # WIP: Output a more descriptive error message
#             #print((node,port,link_id), (peer,peer_port,peer_link_id))
#             assert link_id == peer_link_id 


