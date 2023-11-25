#
# (c) 2022, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.cisco.ios.plugins.modules import ios_interfaces
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args
from ansible_collections.cisco.ios.tests.unit.unit_utils.module_dynamic_test_generator import (
    TestGeneratorFromModuleExamples,
)

from .ios_module import TestIosModule


class TestIosInterfacesModule(TestIosModule):
    module = ios_interfaces

    def setUp(self):
        super(TestIosInterfacesModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.interfaces.interfaces."
            "InterfacesFacts.get_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        self.dynamic_test_obj = TestGeneratorFromModuleExamples(ios_interfaces)

    def tearDown(self):
        super(TestIosInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_interfaces_action_state(self):
        for key, test_vars in self.dynamic_test_obj.action_state_artifact.items():
            self.execute_show_command.return_value = test_vars.get("device_config")
            set_module_args(
                dict(
                    config=test_vars.get("config"),
                    state=test_vars.get("state"),
                ),
            )
            result = self.execute_module(changed=test_vars.get("changed"))

            self.dynamic_test_obj.assert_handler(
                self,
                result["commands"],
                test_vars.get("commands"),
                test_vars.get("state"),
                True,
            )

    def test_ios_interfaces_non_action_state(self):
        for key, test_vars in self.dynamic_test_obj.non_action_state_artifact.items():
            if test_vars.get("state") != "parsed":
                self.execute_show_command.return_value = test_vars.get("device_config")
                module_args_attr = {
                    "config": test_vars.get("config"),
                    "state": test_vars.get("state"),
                }
            else:
                module_args_attr = {
                    "running_config": test_vars.get("device_config"),
                    "state": test_vars.get("state"),
                }
            set_module_args(module_args_attr)
            result = self.execute_module(changed=test_vars.get("changed"))

            self.dynamic_test_obj.assert_handler(
                self,
                result[test_vars.get("state")],
                test_vars.get("commands"),
                test_vars.get("state"),
            )