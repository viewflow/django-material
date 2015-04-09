import os
from fabric.api import env, task, local


BASEDIR = os.path.dirname(env.real_fabfile)


@task
def start_xvfb():
    local('/sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_99.pid'
          '--make-pidfile --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x24')


@task
def generate_baseline_screens(toxenv='django17_py27'):
    start_xvfb()
    local('DISPLAY=:99.0 NEEDLE_SAVE_BASELINE=1 tox {} -- python manage.py test tests.visual'
          .format('-e {}'.format(toxenv) if toxenv else ''))


@task
def test_visual(toxenv='django17_py27'):
    start_xvfb()
    local('DISPLAY=:99.0 tox {} -- python manage.py test tests.visual'
          .format('-e {}'.format(toxenv) if toxenv else ''))


@task
def test_integration(toxenv='django17_py27'):
    local('tox {} -- python manage.py test tests.integration'
          .format('-e {}'.format(toxenv) if toxenv else ''))
