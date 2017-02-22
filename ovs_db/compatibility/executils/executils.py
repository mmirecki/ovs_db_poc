# Do we need this? If we don't use commandline, we can just delete this.

# import os
# if os.name == 'nt':
#    from neutron.agent.windows import utils
# else:
#    from neutron.agent.linux import utils

# execute = utils.execute

# We don't want to use


def execute(cmd, process_input=None, addl_env=None,
            check_exit_code=True, return_stderr=False, log_fail_as_error=True,
            extra_ok_codes=None, run_as_root=False):
    pass
