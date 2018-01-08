from fabric.api import *

env.user = "sysop"
env.hosts = ["ifx.oglam.hasadna.org.il"]


@task
def host_type():
    run("uname -a")


@task
def uptime():
    run("uptime")