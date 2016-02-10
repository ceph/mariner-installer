import subprocess
import tempfile
import logging
from mariner.util import which, get_playbook_path

logger = logging.getLogger(__name__)


def make_ansible_command(hosts_file, identifier, extra_vars='{}', tags=''):
    """
    This utility will compose the command needed to run ansible, capture its
    stdout and stderr to a file
    """
    playbook = get_playbook_path()
    ansible_path = which('ansible-playbook')

    return [
        ansible_path, '-i', hosts_file,
        '--extra-vars="%s"' % extra_vars, '--tags', tags, playbook
    ]


def temp_file(identifier, std):
    return tempfile.NamedTemporaryFile(
        prefix="{identifier}_{std}".format(
            identifier=identifier, std=std), delete=False
    )


def run(arguments, send_input=None, **kwargs):
    """
    A small helper to run a system command using ``subprocess.Popen``.

    This returns the output of the command and the return code of the process
    in a tuple::

        (stdout, stderr, returncode)
    """
    logger.info('Running command: %s' % ' '.join(arguments))
    process = subprocess.Popen(
        arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs)
    if send_input:
        process.communicate(input=send_input)
    out, err = process.communicate()
    return out, err, process.returncode