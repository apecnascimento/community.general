from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible.module_utils.basic import missing_required_lib

import_nomad = None

try:
    import nomad

    import_nomad = True
except ImportError:
    import_nomad = False


def setup_nomad_client(module):
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

    return nomad_client

def transform_token_response(nomad_response):
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


def nomad_auth_argument_spec():
    return dict(
        host=dict(required=True, type='str'),
        port=dict(type='int', default=4646),
        state=dict(required=True, choices=['present', 'absent']),
        use_ssl=dict(type='bool', default=True),
        timeout=dict(type='int', default=5),
        validate_certs=dict(type='bool', default=True),
        client_cert=dict(type='path'),
        client_key=dict(type='path'),
        namespace=dict(type='str'),
        token=dict(type='str', no_log=True)
    )
