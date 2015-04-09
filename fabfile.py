import os
from fabric.api import env, task, local


BASEDIR = os.path.dirname(env.real_fabfile)


@task
def start_xvfb():
    local('/sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_99.pid'
          '--make-pidfile --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x24')


@task
def generate_baseline_screens():
    start_xvfb()
    local('DISPLAY=:99.0 NEEDLE_SAVE_BASELINE=1 tox -e django17_py27 -- python manage.py test tests.visual')


@task
def test_visual():
    start_xvfb()
    local('DISPLAY=:99.0 tox -e django17_py27 -- python manage.py test tests.visual')
