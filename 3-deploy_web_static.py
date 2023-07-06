#!/usr/bin/python3
"""
Defines deploy function.
"""
import os
from datetime import datetime
from fabric.api import local, task, run, put, env, sudo
from os.path import isfile

env.hosts = ['100.25.188.172', '18.209.178.215']


@task
def do_pack():
    """Create a .tgz archive"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists('versions'):
        local("mkdir versions")
    tar_name = "versions/web_static_{}.tgz".format(time)
    result = local("tar -cvzf {} web_static".format(tar_name))

    if result.succeeded:
        return tar_name
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not isfile(archive_path):
        return False
    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]

        put(archive_path, '/tmp/')

        sudo('mkdir -p /data/web_static/releases/{}/'.format(archive_no_ext))

        sudo('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
             .format(archive_filename, archive_no_ext))

        sudo('rm /tmp/{}'.format(archive_filename))

        sudo('mv -f /data/web_static/releases/{}/web_static/* '
             '/data/web_static/releases/{}/'
             .format(archive_no_ext, archive_no_ext))

        sudo('rm -rf /data/web_static/releases/{}/web_static'
             .format(archive_no_ext))

        sudo('rm -rf /data/web_static/current')

        sudo('ln -s /data/web_static/releases/{} '
             '/data/web_static/current'
             .format(archive_no_ext))

        return True

    except Exception as e:
        return False


@task
def deploy():
    """
    Creates and distributes an archive to web servers.
    """
    archive = do_pack()
    if archive is None:
        return False
    else:
        return do_deploy(archive)
