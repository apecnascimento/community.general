#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, Pedro Nascimento <apecnascimento@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: nomad_token_info
author: Pedro Nascimento (@apecnascimento)
version_added: "1.0.0"
short_description: Get Nomad Acl token info
description:
    - Get info for one Nomad acl token.
    - List Acl tokens.
requirements:
  - python-nomad
extends_documentation_fragment:
  - community.general.nomad
  - community.general.attributes
  - community.general.attributes.info_module
options:
    name:
      description:
        - Acl token name.
        - If not specified, lists all tokens.
      type: str
seealso:
  - name: Nomad Acl token documentation
    description: Complete documentation for Nomad API acl token.
    link: https://developer.hashicorp.com/nomad/api-docs/acl/tokens
'''

EXAMPLES = '''
- name: Get info for acl token dev-token
  community.general.nomad_token_info:
    host: localhost
    name: dev-token
  register: token_result

- name: List Nomad Acl tokens
  community.general.nomad_token_info:
    host: localhost
  register: token_list

'''

RETURN = '''
result:
    description: List with dictionary contains token info
    returned: success
    type: list
    sample: [
        
    ]

'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.common.text.converters import to_native

import_nomad = None
try:
    import nomad
    import_nomad = True
except ImportError:
    import_nomad = False


def run():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            port=dict(type='int', default=4646),
            use_ssl=dict(type='bool', default=True),
            timeout=dict(type='int', default=5),
            validate_certs=dict(type='bool', default=True),
            client_cert=dict(type='path'),
            client_key=dict(type='path'),
            namespace=dict(type='str'),
            name=dict(type='str'),
            token=dict(type='str', no_log=True)
        ),
        supports_check_mode=True
    )

    if not import_nomad:
        module.fail_json(msg=missing_required_lib("python-nomad"))

    certificate_ssl = (module.params.get('client_cert'), module.params.get('client_key'))

    nomad_client = nomad.Nomad(
        host=module.params.get('host'),
        port=module.params.get('port'),
        secure=module.params.get('use_ssl'),
        timeout=module.params.get('timeout'),
        verify=module.params.get('validate_certs'),
        cert=certificate_ssl,
        namespace=module.params.get('namespace'),
        token=module.params.get('token')
    )

    changed = False
    result = list()
    try:
    #TODO: implement list tokens
    except Exception as e:
        module.fail_json(msg=to_native(e))


    module.exit_json(changed=changed, result=result)


def main():

    run()


if __name__ == "__main__":
    main()
