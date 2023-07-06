#!/usr/bin/python3
"""
Fabric script to deploy archive to web servers
"""
from os.path import isfile
from fabric.api import run, put, env, sudo

env.hosts = ['100.25.188.172', '18.209.178.215']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file archive_path doesn't exists or case of error - False
        Otherwise - True
    """
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

        sudo('mv /data/web_static/releases/{}/web_static/* '
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
