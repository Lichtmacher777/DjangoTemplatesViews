from django.test import TestCase
from django.urls import reverse
from social_app.models import User, Post
from social_app.form_1 import UserForm, PostForm


class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            bio='This is a test bio.',
            age=25
        )
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'bio': 'This is a new test bio.',
            'age': 30
        }

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_detail_view(self):
        response = self.client.get(
            reverse('user_detail', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'testuser@example.com')

    def test_create_user_view(self):
        response = self.client.post(
            reverse('create_user'), data=self.user_data)
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        self.assertEqual(new_user.age, 30)

    def test_update_user_view(self):
        response = self.client.post(
            reverse('update_user', kwargs={'username': 'testuser'}), data=self.user_data)
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(username='newuser')
        self.assertEqual(updated_user.email, 'newuser@example.com')

    def test_delete_user_view(self):
        response = self.client.post(
            reverse('delete_user', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')


class PostViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            bio='This is a test bio.',
            age=25
        )
        self.post_data = {
            'user': self.user,
            'post': 'This is a test post.',
            'visibility': Post.PUBLIC
        }

    def test_post_list_view(self):
        Post.objects.create(user=self.user, post='This is a test post.')
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social_app/post_list.html')
        # self.assertContains(response, 'This is a test post.')
        # self.assertContains(response, 'testuser')

    def test_post_detail_view(self):
        post = Post.objects.create(
            user=self.user, post='this is a test post', visibility=Post.PUBLIC)
        response = self.client.get(
            reverse('post_detail', kwargs={'post_id': post.id}))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'this is a test post')

    def test_update_post_view(self):
        post = Post.objects.create(
            user=self.user, post='this isOld post', visibility=Post.PUBLIC)
        response = self.client.post(reverse('update_post', kwargs={'username': 'testuser', 'post_id': post.id}),
                                    data={'post': 'Updated post', 'visibility': Post.PUBLIC})
        self.assertEqual(response.status_code, 302)
        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.post, 'Updated post')
        self.assertTemplateUsed('social_app/post_form.html')

    def test_delete_post_view(self):
        post = Post.objects.create(
            user=self.user, post='To be deleted', visibility=Post.PUBLIC)
        response = self.client.post(
            reverse('delete_post', kwargs={'username': 'testuser', 'post_id': post.id}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)
