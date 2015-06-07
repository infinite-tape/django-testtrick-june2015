import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

import praw

from testtrick.apps.kittens.forms import EmailKittenForm


def get_a_kitten():
    '''
    Retrieve a kitten from the Awww subreddt via Reddit's API.
    '''
    # initialize reddit api
    reddit_api = praw.Reddit(user_agent="djangotesttrick")
    # get a handle to the 'Awww' subreddit
    aww_subreddit = reddit_api.get_subreddit("awww")
    kitten_results = aww_subreddit.search("kitten", sort="new", limit=100)

    # sometimes you get self posts, we want to filter those out...
    kittens = [k for k in kitten_results if k.thumbnail != 'self']
    return random.choice(kittens)


def kitten_view(request, *args, **kwargs):
    '''
    Render the kitten.html template with a random kitten from the
    Awww subreddit.
    '''
    the_kitten = get_a_kitten()
    # render the kitten template with the kitten we got
    return render_to_response(
        "kitten.html", {'the_kitten': the_kitten},
        context_instance=RequestContext(request))


def email_a_kitten_view(request, *args, **kwargs):
    '''
    Email the provided email address with a random kitten from the
    Awww subreddit.
    '''
    form = EmailKittenForm()
    if request.method == 'POST':
        # we got a POST, use the POST data to initialize a Form object...
        form = EmailKittenForm(request.POST)
        # check if form data is valid, if so send kittens!
        if form.is_valid():
            the_kitten = get_a_kitten()
            # use send_mail() to email kittens
            num_messages = send_mail(
                "You've received a kitten!",
                render_to_string("kitten_email.txt",
                                 {'the_kitten': the_kitten}),
                settings.SERVER_EMAIL,
                [form.cleaned_data['email']])
            # show a success page
            return render_to_response(
                "kitten_form_success.html",
                {'the_kitten': the_kitten,
                 'num_messages': num_messages,
                 'email': form.cleaned_data['email']},
                context_instance=RequestContext(request))
    # either this isn't a POST request or the form was submitted with invalid
    # data, either way we'll simply render (or re-render) the form template
    return render_to_response(
        "kitten_form.html",
        {'kitten_form': form},
        context_instance=RequestContext(request))
