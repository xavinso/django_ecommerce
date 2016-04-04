"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import mock
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from .views import index
from payments.models import User


class MainPageTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # create a Mock request object, so we can manipulate the session
        # and speed up the testing
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    # ROUTES
    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html(self):
        # index = self.client.get('/')
        # self.assertEquals(index.status_code, 200)
        resp = index(self.request)
        self.assertEquals(
            resp.status_code,
            200
        )

    # Templates and views
    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEquals(
            resp.content,
            render_to_response("index.html").content
        )

    def test_index_handles_logged_in_user(self):
        # create the user needed for user lookup from index page
        user = User(
            name='jj',
            email='j@j.com',
        )
        # As a general rule. you do not want to test the database
        # with a unit test. That would be an integration test.
        # Mocks are perfect for handling calls to the database
        # user.save()

        # create a session that appears to have a logged in user
        self.request.session = {"user": "1"}

        with mock.patch('main.views.User') as user_mock:
            # Tell the mock what to do when called
            config = {'get.return_value': user}
            user_mock.objects.configure_mock(**config)
            # request the index page
            resp = index(self.request)
            # ensure we return the state of the session back to normal so
            # we don't affect other tests
            self.request.session = {}
            # verify it returns the page for the logged in user
            expected_html = render_to_response(
                'user.html',
                {'user': user_mock.get_by_id(1)}
            )
            self.assertEquals(
                resp.content,
                expected_html.content
            )
