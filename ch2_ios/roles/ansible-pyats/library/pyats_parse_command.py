#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection, ConnectionError
from ansible.module_utils.six import PY3
from genie.libs.parser.utils import get_parser_exclude
import json

try:
    from genie.conf.base import Device, Testbed
    from genie.libs.parser.utils import get_parser
    from genie.utils.diff import Diff
    HAS_GENIE = True
except ImportError:
    HAS_GENIE = False

try:
    from pyats.datastructures import AttrDict
    HAS_PYATS = True
except ImportError:
    HAS_PYATS = False

def main():
    argument_spec = dict(command=dict(type='str', required=True),
                prompt=dict(type='list', required=False),
                answer=dict(type='list', required=False),
                compare=dict(type='dict', required=False),
                sendonly=dict(type='bool', default=False, required=False),
                # newline=dict(type='bool', default=True, required=False),
                # check_all=dict(type='bool', default=False, required=False),
    )
    required_together = [['prompt', 'answer']]
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together,
                           supports_check_mode=True)

    if not PY3:
        module.fail_json(msg="pyATS/Genie requires Python 3")

    if not HAS_GENIE:
        module.fail_json(msg="Genie not found. Run 'pip install genie'")

    if not HAS_PYATS:
        module.fail_json(msg="pyATS not found. Run 'pip install pyats'")

    if module.check_mode and not module.params['command'].startswith('show'):
        module.fail_json(
            msg='Only show commands are supported when using check_mode, not '
            'executing %s' % module.params['command']
        )

    warnings = list()
    result = {'changed': False, 'warnings': warnings}

    connection = Connection(module._socket_path)

    capabilities = json.loads(connection.get_capabilities())

    if capabilities['device_info']['network_os'] == 'ios':
        genie_os = 'iosxe'
    else:
        genie_os = capabilities['device_info']['network_os']

    compare = module.params.pop('compare')

    response = ''
    try:
        response = connection.get(**module.params)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))

    device = Device("uut", os=genie_os)

    device.custom.setdefault("abstraction", {})["order"] = ["os"]
    device.cli = AttrDict({"execute": None})

    try:
        get_parser(module.params['command'], device)
    except Exception as e:
        module.fail_json(msg="Unable to find parser for command '{0}' ({1})".format(module.params['command'], e))

    try:
        parsed_output = device.parse(module.params['command'], output=response)
    except Exception as e:
        module.fail_json(msg="Unable to parse output for command '{0}' ({1})".format(module.params['command'], e))

    # import sys;
    # sys.stdin = open('/dev/tty')
    # import pdb;
    # pdb.set_trace()


    if compare:
        diff = Diff(parsed_output, compare, exclude=get_parser_exclude(module.params['command'], device))
        diff.findDiff()
    else:
        diff = None


    if not module.params['sendonly']:
        try:
            result['json'] = module.from_json(response)
        except ValueError:
            pass

        result.update({
            'stdout': response,
            'structured': parsed_output,
            'diff': "{0}".format(diff),
            'exclude': get_parser_exclude(module.params['command'], device),
        })

    module.exit_json(**result)


if __name__ == '__main__':
    main()