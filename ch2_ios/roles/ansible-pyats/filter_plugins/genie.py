from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.six import PY3, string_types
from ansible.errors import AnsibleError, AnsibleFilterError

try:
    from genie.conf.base import Device, Testbed
    from genie.libs.parser.utils import get_parser
    from genie.utils.diff import Diff
    from genie.utils.config import Config
    HAS_GENIE = True
except ImportError:
    HAS_GENIE = False

try:
    from pyats.datastructures import AttrDict
    HAS_PYATS = True
except ImportError:
    HAS_PYATS = False

class FilterModule(object):

    def genie_parser(self, cli_output, command, os):
        if not PY3:
            raise AnsibleFilterError("Genie requires Python 3")

        if not HAS_GENIE:
            raise AnsibleFilterError("Genie not found. Run 'pip install genie'")

        if not HAS_PYATS:
            raise AnsibleFilterError("pyATS not found. Run 'pip install pyats'")

        device = Device("new_device", os=os)

        device.custom.setdefault("abstraction", {})["order"] = ["os"]
        device.cli = AttrDict({"execute": None})

        try:
            get_parser(command, device)
        except Exception as e:
            raise AnsibleFilterError("Unable to find parser for command '{0}' ({1})".format(command, e))

        try:
            parsed_output = device.parse(command, output=cli_output)
        except Exception as e:
            raise AnsibleFilterError("Unable to parse output for command '{0}' ({1})".format(command, e))

        if parsed_output:
            return parsed_output
        else:
            return None

    def genie_config_diff(self, output1, output2, mode=None, exclude=None):
        if not PY3:
            raise AnsibleFilterError("Genie requires Python 3")

        if not HAS_GENIE:
            raise AnsibleFilterError("Genie not found. Run 'pip install genie'")

        if not HAS_PYATS:
            raise AnsibleFilterError("pyATS not found. Run 'pip install pyats'")

        supported_mode = ['add', 'remove', 'modified', None]
        if mode not in supported_mode:
            raise AnsibleFilterError("Mode '%s' is not supported. Specify %s." % (mode, supported_mode) )

        config1 = Config(output1)
        config1.tree()
        dict1 = config1.config

        config2 = Config(output2)
        config2.tree()
        dict2 = config2.config

        dd = Diff(dict1, dict2, mode=mode, exclude=exclude)
        dd.findDiff()
        diff = str(dd)
        diff_list = diff.split('\n')

        return diff_list


    def genie_parser_diff(self, output1, output2, mode=None, exclude=None):
        if not PY3:
            raise AnsibleFilterError("Genie requires Python 3")

        if not HAS_GENIE:
            raise AnsibleFilterError("Genie not found. Run 'pip install genie'")

        if not HAS_PYATS:
            raise AnsibleFilterError("pyATS not found. Run 'pip install pyats'")

        supported_mode = ['add', 'remove', 'modified', None]
        if mode not in supported_mode:
            raise AnsibleFilterError("Mode '%s' is not supported. Specify %s." % (mode, supported_mode) )

        dd = Diff(output1, output2, mode=mode, exclude=exclude)
        dd.findDiff()
        diff = str(dd)
        diff_list = diff.split('\n')

        return diff_list


    def filters(self):
        return {
            'genie_parser': self.genie_parser,
            'genie_config_diff': self.genie_config_diff,
            'genie_parser_diff': self.genie_parser_diff
        }
