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
        - If this or accessor_id are not specified, lists all tokens.
      type: str
    accessor_id:
      description:
        - Acl token AccessorID.
        - If this or name are not specified, lists all tokens.
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


def transform_response(nomad_response):
    transformed_response = {
        "accessor_id": nomad_response['AccessorID'],
        "create_index": nomad_response['CreateIndex'],
        "create_time": nomad_response['CreateTime'],
        "expiration_ttl": nomad_response['ExpirationTTL'],
        "expiration_time": nomad_response['ExpirationTime'],
        "global": nomad_response['Global'],
        "hash": nomad_response['Hash'],
        "modify_index": nomad_response['ModifyIndex'],
        "name": nomad_response['Name'],
        "policies": nomad_response['Policies'],
        "roles": nomad_response['Roles'],
        "secret_id": nomad_response['SecretID'],
        "type": nomad_response['Type']
    }

    return transformed_response


def get_token(module, token_list):
    token = None
    if module.params.get('accessor_id'):
        token = next((token for token in token_list
                      if token.get('accessor_id') == module.params.get('accessor_id')), None)
    if module.params.get('name'):
        token = next((token for token in token_list
                      if token.get('name') == module.params.get('name')), None)

    return token


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
            accessor_id=dict(type='str'),
            token=dict(type='str', no_log=True)
        ),
        supports_check_mode=True,
        required_one_of=[
            ['name', 'accessor_id']
        ]
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
        tokens_list = next((transform_response(token) for token in nomad_client.acl.get_tokens()))
        token = None
        if module.params.get('name') or module.params.get('accessor_id'):
            token = get_token(module, tokens_list)
            if not token:
                module.fail_json(msg="Couldn't find token with name " + str(module.params.get('name')))

            result.append(token)
        else:
            result = tokens_list

    except Exception as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(changed=changed, result=result)


def main():
    run()


if __name__ == "__main__":
    main()
