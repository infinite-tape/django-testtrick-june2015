from django.test import TestCase
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse


class KittenEmailTest(TestCase):

    def setUp(self):
        self.kitten_email_subject = "You've received a kitten!"

    def test_email_kitten_view_post(self):
        '''
        Tests submitting to the email kitten view an email address.
        '''
        response = self.client.post(
            reverse("email-a-kitten"),
            {'email': 'kitten_lord@gmail.com'})
        self.assertEqual(response.status_code, 200)
        # verify there is 1 email in the outbox
        self.assertEqual(len(mail.outbox), 1)
        # verify the correct subject line is on the email
        self.assertEqual(mail.outbox[0].subject, self.kitten_email_subject)
        # verify that the email was sent from correct email address
        self.assertEqual(mail.outbox[0].from_email, settings.SERVER_EMAIL)
