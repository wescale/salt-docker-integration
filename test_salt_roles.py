import logging
import time
from datetime import datetime

import os
import re
import random
import subprocess32 as subprocess
from colored import fg, attr
from nose.tools import assert_equal
from nose.tools import assert_true

SELF_DIR = os.path.dirname(__file__)
ROOT_DIRECTORY = os.environ.get("SALT_PATH", SELF_DIR + "/salt")
ROLES_DIRECTORY = "%s/%s" % (ROOT_DIRECTORY, "states/test")
SALT_MINION_IMAGE = os.environ.get("SALT_MINION_IMAGE", "salt-minion")
SALT_MASTER_IMAGE = os.environ.get("SALT_MASTER_IMAGE", "salt-master")

logger = logging.getLogger('python-docker')

"""
    Automate testing of salt roles
"""


class TestDockerRoles(object):

    def test_salt_roles(self):
        """
            Loop over roles directory and generate a unit test to yield for each one except 'files'
        :return:
        """
        root_dir = ROLES_DIRECTORY
        if 'ROLES' in os.environ:
            dirs = filter(os.path.isdir, [os.path.join(root_dir, f) for f in os.environ['ROLES'].split(',')])
        else:
            dirs = filter(os.path.isdir, [os.path.join(root_dir, f) for f in os.listdir(root_dir) if f != 'files'])
        for directory in dirs:
            logger.info(directory)
            yield exec_role, re.sub('^.*/', '', directory)


def tear_down(minion_id):
    logger.info("clear minion container " + minion_id)
    exec_shell('docker rm -fv {minion_id}'.format(minion_id=minion_id))


def launch_master():
    """
        Launch the master container we will use for all tests
    """
    master_id = "salt_master_%s_%s" % (datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), str(random.randint(0, 100000000)))
    out, err, returncode = exec_shell('docker run -tid --name="{master_id}" '
                                      '-v {root_dir}:/srv/salt {salt_image}'
                                      .format(master_id=master_id, root_dir=ROOT_DIRECTORY,
                                              salt_image=SALT_MASTER_IMAGE))
    out, err, returncode = exec_shell("docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + master_id)
    master_ip = out

    return master_id, master_ip


def kill_master(master_id):
    """
        Force kill salt master after class tests
    """
    exec_shell('docker rm -fv {master_id}'.format(master_id=master_id))


def setup_for_role(role_dir, master_ip):
    """
        Prepare environment for testing a specific salt role:
        remove previously existing keys for this role in master
        Generate a new grains file to mount in container
        Generate a new minion.conf file to mount in container
    :param master_ip: Ip of the master container
    :param role_dir: Name of the role to test
    :return:
    """
    minion_id = "%s_%s" % (role_dir, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    grains_path = os.path.join(ROLES_DIRECTORY, role_dir, 'grains')
    test_grains_path = os.path.join(ROLES_DIRECTORY, role_dir, 'test_grains')
    minion_path = os.path.join(ROLES_DIRECTORY, role_dir, 'minion.conf')
    global_minion_path = os.path.join(ROLES_DIRECTORY, 'files', 'minion.conf')

    # Remove grains file
    try:
        os.remove(grains_path)
    except:
        pass
    try:
        os.remove(minion_path)
    except:
        pass

    # Generate grains file for minion
    with open(grains_path, "a") as grains:
        grains.write("""
salt_id: {minion_id}
name: {minion_id}
salt_master: {salt_master}
env: docker
""".format(minion_id=minion_id, salt_master=master_ip))
        with open(test_grains_path) as test_grains:
            grains.write(test_grains.read())
            grains.write(os.linesep)

    # Generate minion.conf file for minion
    with open(minion_path, "a") as minion_conf:
        minion_conf.write("""
id: {minion_id}
master: {salt_master}
""".format(minion_id=minion_id, salt_master=master_ip))

    return minion_id


def write_if_exist(grains, grains_dict, key):
    mirror = grains_dict.get(key)
    if mirror is not None:
        grains.write(key + ': ' + mirror + os.linesep)


def exec_shell(cmd, log=False):
    """
        Execute a command in shell, print its output and return stdout, stderr, and return code
    :param cmd:
    :param log:
    :return:
    """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if log:
        logger.info(cmd)
        logger.info(out)

        if err:
            logger.error("%s%s%s" % (fg('red'), err, attr('reset')))
        logger.info("exit: %d" % process.returncode)

    return out, err, process.returncode


def validate_salt(output):
    """
        Validate the output of a salt cli with assertions this compare success states against total count of ran states
    :param output:
    :return:
    """
    nb_ok = len(re.findall('Failed:\W*[0]', output))
    nb_states = len(re.findall('Failed:\W*[^0]', output))
    assert_equal(nb_ok, nb_states, "%d state failed on %d total states" % (nb_states - nb_ok, nb_states))


def exec_role(role_dir):
    """
        Unit test for a specific salt role, this spawns a new container populated with specific minion.conf and grains
        specified for the role. Then it applies a highstate on the new container and on success applies asserts.sls
        to ensure the role is working as expect
    :param role_dir: directory name for the role to test
    """
    logger.info("Running test for role " + role_dir)

    master_id, master_ip = launch_master()

    role_abs_dir = os.path.join(ROLES_DIRECTORY, role_dir)
    minion_id = setup_for_role(role_dir, master_ip)
    try:
        # Launch the container we will use for highstate test
        out, err, returncode = exec_shell('docker run -tid --name="{minion_id}" '
                                          '--privileged -v {role_dir}/minion.conf:/etc/salt/minion.d/minion.conf '
                                          '-v {role_dir}/grains:/etc/salt/grains '
                                          '-v /sys/fs/cgroup:/sys/fs/cgroup:ro {salt_image}'
                                          .format(minion_id=minion_id, role_dir=role_abs_dir,
                                                  salt_image=SALT_MINION_IMAGE))
        assert_true(returncode == 0, "Role container should be spawned without error")
        time.sleep(10)

        # Ping salt minion in container before applying highstate
        for i in range(0, 10):
            out, err, returncode = exec_shell(
                'docker exec -i {master_id} salt "{minion_id}" -t 30 test.ping --output yaml'.format(
                    master_id=master_id, minion_id=minion_id))
            ping_result = out
            if 'true' in out:
                break

        assert_true(ping_result, "Minion container should ping from master via salt test.ping")

        # Refresh states
        out, err, returncode = exec_shell(
            'docker exec -i {master_id} salt "{minion_id}" saltutil.sync_all --force-color'
            ' --state-output=mixed'
            .format(master_id=master_id, minion_id=minion_id))

        assert_true(returncode == 0, "Sync all execution should return code 0")

        # Refresh pillars
        out, err, returncode = exec_shell(
            'docker exec -i {master_id} salt "{minion_id}" saltutil.pillar_refresh --force-color'
            ' --state-output=mixed'
            .format(master_id=master_id, minion_id=minion_id))

        assert_true(returncode == 0, "Pillar refresh execution should return code 0")

        # Apply highstate to the container
        out, err, returncode = exec_shell(
            'docker exec -i {master_id} salt "{minion_id}" -t 30 state.highstate --force-color'
            ' --state-output=mixed'
            .format(master_id=master_id, minion_id=minion_id), log=True)

        assert_true(returncode == 0, role_dir + " Highstate execution should return code 0")
        validate_salt(out)

        # Only apply asserts.sls when it is present
        if os.path.isfile("{roles_dir}/{role}/asserts.sls".format(roles_dir=ROLES_DIRECTORY, role=role_dir)):
            # Apply asserts.sls to ensure role does work as expected
            out, err, returncode = exec_shell(
                'docker exec -i {master_id} salt "{minion_id}" -t 30 state.sls test.{role}.asserts'
                ' --force-color --state-output=mixed'
                .format(master_id=master_id, minion_id=minion_id, role=role_dir), log=True)
            assert_true(returncode == 0, role_dir + " asserts.sls execution should return code 0")
            validate_salt(out)
    finally:
        tear_down(minion_id)
        kill_master(master_id)