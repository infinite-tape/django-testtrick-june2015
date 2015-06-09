import re
from django.test import TestCase, override_settings
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from httpretty import HTTPretty


MOCK_RESPONSE = '''
    {
        "kind": "Listing",
        "data": {
            "modhash": "",
            "children": [
            {
                "kind": "t3",
                "data": {
                    "domain": "imgur.com",
                    "banned_by": null,
                    "media_embed": {},
                    "subreddit": "aww",
                    "selftext_html": null,
                    "selftext": "",
                    "likes": null,
                    "suggested_sort": null,
                    "user_reports": [],
                    "secure_media": null,
                    "link_flair_text": null,
                    "id": "1i9si4",
                    "from_kind": null,
                    "gilded": 0,
                    "archived": true,
                    "clicked": false,
                    "report_reasons": null,
                    "author": "kitten-little",
                    "media": null,
                    "score": 731,
                    "approved_by": null,
                    "over_18": false,
                    "hidden": false,
                    "num_comments": 16,
                    "thumbnail": "http://b.thumbs.redditmedia.com/5qjC7z6GpHGy5OZa.jpg",
                    "subreddit_id": "t5_2qh1o",
                    "edited": false,
                    "link_flair_css_class": null,
                    "author_flair_css_class": null,
                    "downs": 0,
                    "secure_media_embed": {},
                    "saved": false,
                    "removal_reason": null,
                    "stickied": false,
                    "from": null,
                    "is_self": false,
                    "from_id": null,
                    "permalink": "/r/aww/comments/1i9si4/the_saddest_kitten_in_the_world_she_sleeps_on_my/?ref=search_posts",
                    "name": "t3_1i9si4",
                    "created": 1373804881,
                    "url": "http://imgur.com/a/9gsNn",
                    "author_flair_text": null,
                    "title": "The saddest kitten in the world. She sleeps on my shoulder. (x-post r/cats)",
                    "created_utc": 1373801281,
                    "distinguished": null,
                    "mod_reports": [],
                    "visited": false,
                    "num_reports": null,
                    "ups": 731
                }
            }
            ],
            "after": "t3_290y45",
            "before": null
        }
    }
'''

class KittenTest(TestCase):

    def setUp(self):
        '''
        Mock-out our Reddit API endpoint.
        '''
        self.kitten_email_subject = "You've received a kitten!"
        HTTPretty.enable()
        HTTPretty.allow_net_connect = False
        HTTPretty.register_uri(
            HTTPretty.GET,
            "www.reddit.com/r/Awww/search/.json",
            body=MOCK_RESPONSE,
            content_type='application/json')

    def tearDown(self):
        HTTPretty.disable()
        HTTPretty.reset()

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

    @override_settings(SERVER_EMAIL='no-reply@yahoo.com')
    def test_email_kitten_from_email(self):
        '''
        Test that changing settings.SERVER_EMAIL results in a different From:
        address in our kitten emails.
        '''
        response = self.client.post(
            reverse("email-a-kitten"),
            {'email': 'kitten_lord@gmail.com'})
        # internally the view should be using settings.SERVER_EMAIL as the
        # from address, so if we override it with something hard-coded, the
        # email should be sent from the override
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@yahoo.com')

    def test_kitten_view(self):
        '''
        Tests that the kitten view is displaying a kitten from reddit!
        '''
        response = self.client.post(reverse("show-a-kitten"))
        self.assertIn("The saddest kitten in the world",
                      response.content.decode("utf8"))
