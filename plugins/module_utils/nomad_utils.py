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
