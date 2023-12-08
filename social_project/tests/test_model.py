from django.test import TestCase
from social_app.models import User,Post
from django.utils import timezone
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):
    def setUp(self) :
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'This is a test bio.',
            'age': 25
        }
    def tearDown(self) :
        User.objects.all().delete()
        
    
    
    def test_user_creation(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.bio, 'This is a test bio.')
        self.assertEqual(user.age, 25)
        self.assertIsNotNone(user.joined_at)
        self.assertTrue(isinstance(user.joined_at,timezone.datetime))
        
    def test_user_validation_bad_words(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='badword', email='badword@example.com', bio='This contains a bad word: cat')
        
    def test_user_validation_age(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='testuser', email='testuser@example.com', bio='Valid bio', age=10)
        with self.assertRaises(ValidationError):
            User.objects.create(username='testuser', email='testuser@example.com', bio='Valid bio', age=101)
    
    def test_user_validation_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='testuser', email='testuser@example.what', bio='Valid bio', age=25)

class PostModelTest(TestCase):
    def setUp(self) :
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
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
    def test_post_creation(self):
        post = Post.objects.create(**self.post_data)
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.post, 'This is a test post.')
        self.assertEqual(post.visibility, Post.PUBLIC)
        self.assertIsNotNone(post.created_at)
        self.assertIsInstance(post.created_at, timezone.datetime)
    def test_post_validation_length(self):
        with self.assertRaises(ValidationError):
            Post.objects.create(user=self.user, post='Short', visibility=Post.PUBLIC)
    def test_post_validation_bad_words(self):
        with self.assertRaises(ValidationError):
            Post.objects.create(user=self.user, post='This post contains a bad word: dog', visibility=Post.PUBLIC)