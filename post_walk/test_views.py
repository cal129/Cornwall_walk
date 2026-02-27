from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import postwalk


class TestWalkViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.walk = postwalk(
            title="Walk title",
            user=self.user,
            slug="walk-title",
            description="Walk description",
            distance=5.0,
            time_hours=2,
            time_minutes=30,
            difficulty=1,
            type=1,
            location="Cornwall",
            coordinates="50.4155° N, 5.0737° W",
            authorised=True
        )
        self.walk.save()

    def test_render_walk_detail_page_with_comment_form(self):
        response = self.client.get(reverse(
            'walk_detail', args=['walk-title']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Walk title", response.content)
        self.assertIn(b"Walk description", response.content)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

    def test_unauthenticated_user_cannot_comment(self):
        self.client.logout()
        response = self.client.post(reverse('walk_detail', args=['walk-title']),
            {'content': 'Test comment'})
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_walk_not_visible(self):
        walk = postwalk.objects.create(
            title="Hidden", user=self.user, slug="hidden",
            description="Test", distance=1, time_hours=1, time_minutes=0,
            difficulty=1, type=1, location="Test", coordinates="50.4° N, 5.0° W",
            authorised=False
        )
        response = self.client.get(reverse('walk_list'))
        self.assertNotIn(b"Hidden", response.content)
