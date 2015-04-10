import os
from needle.cases import NeedleTestCase

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class VisualTest(NeedleTestCase, StaticLiveServerTestCase):
    def assertScreenshot(self, element_or_selector, file, threshold=1):
        try:
            super(VisualTest, self).assertScreenshot(element_or_selector, file, threshold)
        except:
            baseline_file = os.path.join(self.baseline_directory, '%s.png' % file)
            output_file = os.path.join(self.output_directory, '%s.png' % file)

            message = EmailMessage('Failed {}'.format(self), 'Compare images:',
                                   settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])

            message.attach_file(baseline_file)
            message.attach_file(output_file)

            settings.EMAIL_BACKEND = mail._original_email_backend
            message.send(fail_sliently=True)
            settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

            raise
