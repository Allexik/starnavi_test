from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from posts.models import Post, Comment


class TestPostViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', user=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New post content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_update_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_update_post_by_different_user(self):
        second_user = User.objects.create_user(username='seconduser', password='secondpassword')
        self.client.logout()
        self.client.login(username='seconduser', password='secondpassword')

        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Unauthorized Update Title'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCommentViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', user=self.user)
        self.comments = Comment.objects.bulk_create([
            Comment(content='Test Comment 1', post=self.post, user=self.user),
            Comment(content='Test Comment 2', post=self.post, user=self.user),
            Comment(content='Test Comment 3', post=self.post, user=self.user),
            Comment(content='Test Comment 4', post=self.post, user=self.user, blocked=True),
            Comment(content='Test Comment 5', post=self.post, user=self.user, blocked=True)
        ])
        self.client.login(username='testuser', password='testpassword')

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'content': 'New Comment', 'post': self.post.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(content='New Comment').exists())

    def test_update_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comments[0].pk})
        data = {'content': 'Updated Comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comments[0].refresh_from_db()
        self.assertEqual(self.comments[0].content, 'Updated Comment')

    def test_delete_comment(self):
        url = reverse('comment-detail', kwargs={'pk': self.comments[0].pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comments[0].pk).exists())

    def test_daily_breakdown(self):
        url = reverse('comment-daily-breakdown')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        breakdown = response.data[0]
        self.assertEqual(breakdown['comment_count'], 5)
        self.assertEqual(breakdown['blocked_count'], 2)

    def test_update_comment_by_different_user(self):
        second_user = User.objects.create_user(username='seconduser', password='secondpassword')
        self.client.logout()
        self.client.login(username='seconduser', password='secondpassword')

        url = reverse('comment-detail', kwargs={'pk': self.comments[0].pk})
        data = {'content': 'Unauthorized Updated Comment'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestServices(APITestCase):
    def test_check_text_inappropriateness(self):
        from posts.services import check_text_inappropriateness
        self.assertFalse(check_text_inappropriateness('This is an appropriate comment.'))
        if settings.INAPPROPRIATE_TEXT:
            self.assertTrue(check_text_inappropriateness(settings.INAPPROPRIATE_TEXT))

    def test_generate_comment_answer(self):
        from posts.services import generate_comment_answer
        post_title = 'Test Post'
        post_content = 'Test Content'
        comment_content = 'This is a comment.'
        answer = generate_comment_answer(post_title, post_content, comment_content)
        self.assertTrue(answer)
        self.assertIsInstance(answer, str)
