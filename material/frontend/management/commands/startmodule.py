import errno
import io
import shutil
import six
import os
from importlib import import_module
from os import path

import django
from django.conf import settings
from django.template import Context, Engine
from django.core.management.base import CommandError
from django.core.management.utils import handle_extensions
from django.core.management.templates import TemplateCommand

import material


class Command(TemplateCommand):
    help = (
        "Create a Frontend Module directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."
    rewrite_template_suffixes = (
        ('.py-tpl', '.py'),
        ('.html-tpl', '.html'),
    )

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.set_defaults(extensions=['py', 'html'])

    def handle_template(self, template, subdir):
        """
        Determine where the app or project templates are.

        Use django.__path__[0] as the default because we don't
        know into which directory Django has been installed.
        """
        if template is None:
            return path.join(material.__path__[0], 'conf', subdir)
        return super(Command, self).handle_template(template, subdir)

    def _validate_name(self, app_name):
        super(Command, self).validate_name(app_name, "module")
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError(
                "%r conflicts with the name of an existing Python module and "
                "cannot be used as an app name. Please try another name." % app_name
            )

    def _expand_target_dir(self, app_name, target):
        if target is None:
            top_dir = path.join(os.getcwd(), app_name)
            try:
                os.makedirs(top_dir)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    message = "'%s' already exists" % top_dir
                else:
                    message = e
                raise CommandError(message)
        else:
            top_dir = os.path.abspath(path.expanduser(target))
            if not os.path.exists(top_dir):
                raise CommandError("Destination directory '%s' does not "
                                   "exist, please create it first." % top_dir)
        return top_dir

    def handle(self, **options):
        self.verbosity = options['verbosity']
        app_name, target = options.pop('name'), options.pop('directory')
        extensions = tuple(handle_extensions(options['extensions']))
        extra_files = []
        for file in options['files']:
            extra_files.extend(map(lambda x: x.strip(), file.split(',')))

        self._validate_name(app_name)

        self.paths_to_remove = []
        top_dir = self._expand_target_dir(app_name, target)

        camel_case_app_name = ''.join(x for x in app_name.title() if x != '_')
        context = Context(dict(options, **{
            'app_name': app_name,
            'camel_case_app_name': camel_case_app_name,
            'base_directory': top_dir,
            'unicode_literals': '' if six.PY3 else '# -*- coding: utf-8 -*-\n'
                                                   'from __future__ import unicode_literals\n\n',
        }), autoescape=False)

        # Setup a stub settings environment for template rendering
        if not settings.configured:
            settings.configure()
            django.setup()

        template_dir = self.handle_template(options['template'], 'module_template')
        prefix_length = len(template_dir) + 1

        for root, dirs, files in os.walk(template_dir):
            path_rest = root[prefix_length:]
            relative_dir = path_rest.replace('module_name', app_name)
            if relative_dir:
                target_dir = path.join(top_dir, relative_dir)
                if not path.exists(target_dir):
                    os.mkdir(target_dir)

            for filename in files:
                old_path = path.join(root, filename)
                new_path = path.join(top_dir, relative_dir, filename.replace('module_name', app_name))

                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path[:-len(old_suffix)] + new_suffix
                        break  # Only rewrite once

                if path.exists(new_path):
                    raise CommandError(
                        "{} already exists, overlaying a project or app into an existing "
                        "directory won't replace conflicting files".format(new_path))

                if new_path.endswith(extensions) or filename in extra_files:
                    with io.open(old_path, 'r', encoding='utf-8') as template_file:
                        content = template_file.read()
                    template = Engine().from_string(content)
                    content = template.render(context)
                    with io.open(new_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(content)
                else:
                    shutil.copyfile(old_path, new_path)

                if self.verbosity >= 2:
                    self.stdout.write("Creating %s\n" % new_path)
                try:
                    shutil.copymode(old_path, new_path)
                    self.make_writeable(new_path)
                except OSError:
                    self.stderr.write(
                        "Notice: Couldn't set permission bits on %s. You're "
                        "probably using an uncommon filesystem setup. No "
                        "problem." % new_path, self.style.NOTICE)

        if self.paths_to_remove:
            if self.verbosity >= 2:
                self.stdout.write("Cleaning up temporary files.\n")
            for path_to_remove in self.paths_to_remove:
                if path.isfile(path_to_remove):
                    os.remove(path_to_remove)
                else:
                    shutil.rmtree(path_to_remove)

        if self.verbosity >= 1:
            self.stdout.write("{} module created\n" .format(camel_case_app_name))
            self.stdout.write(
                "To enable the module you need to add '{}.apps.{}Config' "
                "to the INSTALLED_APPS setting".format(app_name, camel_case_app_name))
            self.stdout.write('and run ./manage.py migrate after that\n')
