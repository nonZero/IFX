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


env.venv_name = "IFX"
env.venvs = f"/home/sysop/.virtualenvs/"
env.venv_path = f"{env.venvs}{env.venv_name}/"
env.venv_command = f"source {env.venv_path}/bin/activate"

@task
def create_venv():
    run(f"mkdir -p {env.venvs}")
    run(f"virtualenv -p /usr/bin/python3 --prompt='({env.venv_name}) ' {env.venv_path}")

from contextlib import contextmanager

@contextmanager
def virtualenv():
    with cd(env.code_dir):
        with prefix(env.venv_command):
            yield

@task
def upgrade_pip():
    with virtualenv():
        run("pip install --upgrade pip", pty=False)

@task
def pip_install():
    with virtualenv():
        run("pip install -r requirements.txt", pty=False)

@task
def m(cmd, pty=False):
    with virtualenv():
        run(f"./manage.py {cmd}", pty=pty)

@task
def check():
    m('check')

@task
def send_test_mail():
    m('sendtestemail --admin')

@task
def createsuperuser():
    m('createsuperuser', True)


@task
def git_pull():
    with virtualenv():
        run("git pull", pty=False)

@task
def create_db():
    with virtualenv():
        run("./manage.py sqlcreate | psql", pty=False)
