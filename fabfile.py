from fabric.api import *

env.user = "sysop"
env.hosts = ["ifx.oglam.hasadna.org.il"]


@task
def host_type():
    run("uname -a")

APT_PACKAGES = [
    # generic system related packages
    'unattended-upgrades',  # for auto updating your system
    'ntp',  # To keep time synchromized
    'fail2ban',  # to secure against SSH/other attacks

    'postfix',  # mail server
    'opendkim',  # SSL for mail
    'opendkim-tools',

    # useful tools
    'git',
    'htop',
    'most',

    'python3',
    'virtualenvwrapper',  # for easily managing virtualenvs

    # required libraries for building some python packages
    'build-essential',
    'python3-dev',
    'libpq-dev',
    'libjpeg-dev',
    'libjpeg8',
    'zlib1g-dev',
    'libfreetype6',
    'libfreetype6-dev',
    'libgmp3-dev',

    # postgres database
    'postgresql',

    'nginx',  # a fast web server
    'uwsgi',  # runs python (django) apps via WSGI

    'rabbitmq-server',  # for offline tasks via celery
]

@task
def apt_install():
    pkgs = " ".join(APT_PACKAGES)
    sudo(f"DEBIAN_FRONTEND=noninteractive apt-get install -y -q {pkgs}", pty=False)

@task
def uptime():
    run("uptime")
    
@task
def apt_upgrade():
    sudo("apt-get update", pty=False)
    sudo("apt-get upgrade -y", pty=False)

@task
def create_postgres_su():
    run("sudo -u postgres createuser -s sysop")
    run("createdb sysop")
    

env.project = "IFX"
env.code_dir = f"/home/sysop/{env.project}"
env.clone_url = "https://github.com/IFXGlam/IFX.git"

@task
def clone_project():
    run(f"git clone {env.clone_url} {env.code_dir}", pty=False)