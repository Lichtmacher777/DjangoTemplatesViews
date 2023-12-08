from django.test import TestCase
from social_app.models import User, Post
from social_app.form_1 import UserForm, PostForm

class UserFormTest(TestCase):
    def test_valid_user_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'This is a test bio.',
            'age': 25
        }
        form = UserForm(data=form_data)
        
        
    def test_invalid_user_form_bad_words(self):
        form_data = {
            'username': 'badword',
            'email': 'badword@example.com',
            'bio': 'This contains a bad word: cat',
            'age': 30
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('bio', form.errors)
        
    def test_invalid_user_form_age(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'Valid bio',
            'age': 10
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)
        
    def test_invalid_user_form_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.what',
            'bio': 'Valid bio',
            'age': 25
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class PostFormTest(TestCase):
    def setUp(self):
            self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            bio='This is a test bio.',
            age=25
        )
    def test_valid_post_form(self):
        form_data = {
            'post': 'This is a valid post.',
            'visibility': Post.PUBLIC
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
    def test_invalid_post_form_length(self):
        form_data = {
            'user':self.user,
            'post': 'Short',
            'visibility': Post.PUBLIC
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_invalid_post_form_bad_words(self):
        form_data = {
            'user':self.user,
            'post': 'This post contains a bad word: dog',
            'visibility': Post.PUBLIC
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())