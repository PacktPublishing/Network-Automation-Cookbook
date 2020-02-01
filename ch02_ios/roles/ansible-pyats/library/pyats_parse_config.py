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
import json

try:
    from genie.conf.base import Device, Testbed
    from genie.libs.parser.utils import get_parser
    from genie.utils.diff import Diff
    from genie.libs.parser.utils import get_parser_exclude
    from genie.utils.config import Config
    HAS_GENIE = True
except ImportError:
    HAS_GENIE = False

try:
    from pyats.datastructures import AttrDict
    HAS_PYATS = True
except ImportError:
    HAS_PYATS = False

def main():
    argument_spec = dict(compare=dict(type='dict', required=False),
                sendonly=dict(type='bool', default=False, required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
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

    response = ''
    try:
        response = connection.get(command='show run')
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))

    config = Config(response)
    config.tree()

    if module.params['compare']:
        diff = Diff(config.config, module.params['compare'])
        diff.findDiff()
    else:
        diff = None

    try:
        result['json'] = module.from_json(response)
    except ValueError:
        pass

    result.update({
        'stdout': response,
        'structured': config.config,
        'diff': "{0}".format(diff)
    })

    module.exit_json(**result)


if __name__ == '__main__':
    main()