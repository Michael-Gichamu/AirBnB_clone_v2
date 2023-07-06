#!/usr/bin/python3
"""
Generate a .tgz archive from the contents of web_static folder
"""
import os
from datetime import datetime
from fabric.api import local, task


@task
def do_pack():
    """Create a .tgz archive from contents of the web_static folder"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists('versions'):
        local("mkdir versions")
    tar_name = "versions/web_static_{}.tgz".format(time)
    result = local("tar -cvzf {} web_static".format(tar_name))

    if result.succeeded:
        return tar_name
    else:
        return None
