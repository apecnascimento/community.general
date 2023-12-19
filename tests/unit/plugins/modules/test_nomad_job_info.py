from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.general.plugins.modules import nomad_job_info
from ansible_collections.community.general.tests.unit.compat.mock import patch
from ansible_collections.community.general.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)


class TestNomadJobInfoModule(ModuleTestCase):
    def setUp(self):
        super(TestNomadJobInfoModule, self).setUp()
        self.module = nomad_job_info

    def tearDown(self):
        super(TestNomadJobInfoModule, self).tearDown()

    def test_should_fail_without_parameters(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()
