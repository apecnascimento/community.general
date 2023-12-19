from __future__ import absolute_import, division, print_function

__metaclass__ = type

import nomad
from requests import Response
from ansible_collections.community.general.plugins.modules import nomad_job
from ansible_collections.community.general.tests.unit.compat.mock import patch
from ansible_collections.community.general.tests.unit.plugins.modules.utils import AnsibleExitJson, AnsibleFailJson, \
    ModuleTestCase, \
    set_module_args

def create_hcl_job():
    hcl_job = '''
job "whoami" {
  datacenters = ["dc1"]

  group "whoami" {
    network {
      port "web" { to = 80 }
    }

    service {
      name = "whoami"
      port = "web"
   }

    task "whoami" {
      driver = "docker"

      config {
        image = "traefik/whoami"
        ports = ["api"]
      }

      resources {
        cpu    = 500
        memory = 256
      }
    }
  }
}
'''
    return hcl_job


def create_json_job():
    job = '''
{
    "Datacenters": ["dc1"],
    "ID": "cache",
    "NodePool": "prod",
    "TaskGroups": [
      {
        "Name": "cache",
        "Networks": [
          {
            "DynamicPorts": [
              {
                "Label": "db",
                "To": 6379
              }
            ]
          }
        ],
        "Services": [
          {
            "Name": "redis-cache",
            "PortLabel": "db"
          }
        ],
        "Tasks": [
          {
            "Config": {
              "image": "redis:7",
              "ports": ["db"]
            },
            "Driver": "docker",
            "Name": "redis"
          }
        ]
      }
    ]
}
'''
    return job


def mock_result_parse():
    job = {
"job": [
    {
    "whoami": [
        {
        "datacenters": [
            "dc1"
        ],
        "group": [
            {
            "whoami": [
                {
                "network": [
                    {
                    "port": [
                        {
                        "web": [
                            {
                            "to": 80
                            }
                        ]
                        }
                    ]
                    }
                ],
                "service": [
                    {
                    "name": "whoami",
                    "port": "web"
                    }
                ],
                "task": [
                    {
                    "whoami": [
                        {
                        "config": [
                            {
                            "image": "traefik/whoami",
                            "ports": [
                                "api"
                            ]
                            }
                        ],
                        "driver": "docker",
                        "resources": [
                            {
                            "cpu": 500,
                            "memory": 256
                            }
                        ]
                        }
                    ]
                    }
                ]
                }
            ]
            }
        ]
        }
    ]
    }
]
}

    return job


def mock_result_plan_job():
    mock_result = {
        'Diff': { 'Type': 'Added' }
    }
    return mock_result


def mock_result_register_job():
    mock_result = {
        "EvalID": "",
        "EvalCreateIndex": 0,
        "JobModifyIndex": 109,
        "Warnings": "",
        "Index": 0,
        "LastContact": 0,
        "KnownLeader": False
    }
    return mock_result

class TestNomadJobModule(ModuleTestCase):

    def setUp(self):
        super(TestNomadJobModule, self).setUp()
        self.module = nomad_job


    def tearDown(self):
        super(TestNomadJobModule, self).tearDown()


    def test_should_fail_without_parameters(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    def test_should_create_hcl_job(self):
        module_args = {
            'host': 'localhost',
            'state': 'present',
            'content_format': 'hcl',
            'content': create_hcl_job()
        }

        set_module_args(module_args)
        with patch.object(nomad.api.Job, 'plan_job') as mock_plan_job:
            with patch.object(nomad.api.Jobs, 'register_job') as mock_register_job:
                with patch.object(nomad.api.Jobs, 'parse') as mock_parse:
                    mock_plan_job.return_value = mock_result_plan_job()
                    mock_register_job.return_value = mock_result_register_job()
                    mock_parse.return_value = mock_result_parse()
                    with self.assertRaises(AnsibleExitJson):
                        self.module.main()  
                    self.assertIs(mock_plan_job.call_count, 1)
                    self.assertIs(mock_register_job.call_count, 1)

    def test_should_create_json_job(self):
        module_args = {
            'host': 'localhost',
            'state': 'present',
            'content_format': 'json',
            'content': create_json_job()
        }

        set_module_args(module_args)
        with patch.object(nomad.api.Job, 'plan_job') as mock_plan_job:
            with patch.object(nomad.api.Jobs, 'register_job') as mock_register_job:
                mock_plan_job.return_value = mock_result_plan_job()
                mock_register_job.return_value = mock_result_register_job()
                with self.assertRaises(AnsibleExitJson):
                    self.module.main()  
                self.assertIs(mock_plan_job.call_count, 1)
                self.assertIs(mock_register_job.call_count, 1)

