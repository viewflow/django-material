import os
from fabric.api import env, task, local


BASEDIR = os.path.dirname(env.real_fabfile)


@task
def start_xvfb():
    local('/sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_99.pid'
          '--make-pidfile --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x16')


@task
def generate_baseline_screens(toxenv='django18_py27', test=''):
    start_xvfb()
    local('DISPLAY=:99.0 NEEDLE_SAVE_BASELINE=1 tox {} -- python manage.py test tests.visual{}'
          .format('-e {}'.format(toxenv) if toxenv else '',
                  '.tests.{}'.format(test) if test else ''))


@task
def test_visual(toxenv='django18_py27', test=''):
    start_xvfb()
    local('DISPLAY=:99.0 tox {} -- python manage.py test tests.visual{}'
          .format('-e {}'.format(toxenv) if toxenv else '',
                  '.tests.{}'.format(test) if test else ''))


@task
def test_integration(toxenv='django18_py27', test=''):
    local('tox {} -- python manage.py test tests.integration{}'
          .format('-e {}'.format(toxenv) if toxenv else '',
                  '.tests.{}'.format(test) if test else ''))
