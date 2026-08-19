#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os


def main():

    module = AnsibleModule(
        argument_spec=dict(
            path=dict(
                type='str',
                required=True
            )
        ),
        supports_check_mode=True
    )

    path = module.params['path']

    if not os.path.exists(path):
        module.fail_json(
            msg=f"Status file {path} does not exist"
        )

    try:
        with open(path, 'r') as file:
            status = file.read().strip()

    except Exception as error:
        module.fail_json(
            msg=f"Unable to read status file: {error}"
        )

    healthy = status == "RUNNING"

    module.exit_json(
        changed=False,
        healthy=healthy,
        status=status,
        message=f"Application status is {status}"
    )


if __name__ == '__main__':
    main()