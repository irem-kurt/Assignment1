from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from authenticate.models import Profile
from socio.forms import CommunityForm, DefaultPostForm
from socio.models import Community, Post
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

class CommunityCreateViewTest(TestCase):
    def setUp(self):
        # Create a test user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        user_profile = Profile(user=test_user1, id=test_user1.id, name="Test User")
        user_profile.save()


    def test_get_request(self):
        # Test GET request to the view
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('community-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'socio/communitycreate.html')
        self.assertIsInstance(response.context['form'], CommunityForm)

    def test_post_request_valid_form(self):
        # Test POST request with valid form data
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        
        # create mock image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='PNG', filename='mock_image.png')
        image_io.seek(0)
        
        form_data = {
            'name': 'Test Community',
            'description': 'Test Description',
            'rules': 'Test rules for the community',
            'location': '41.05, 44,10',
            'is_private': False,
            'picture': SimpleUploadedFile(
                'mock_image.png',
                image_io.read()
            )  # You can provide a mock image file if needed
        }
        response = self.client.post(reverse('community-create'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Community.objects.filter(name='Test Community').exists())


class CreatePostViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user1.save()


        # Assuming Profile model exists
        user_profile = Profile.objects.create(user=self.test_user1, name="Test User")
        user_profile.save()
        self.test_user1.profile = user_profile
        self.test_user1.save()
        # Create a community
        self.community = Community.objects.create(name='Test Community', description='Test Description', owner=self.test_user1)
        
    def test_get_request(self):
        # Test GET request to the view
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create_post', args=[self.community.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'socio/create_post.html')
        self.assertIsInstance(response.context['form'], DefaultPostForm)

    def test_post_request_valid_form(self):
        # Test POST request with valid form data
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description',
        }
        response = self.client.post(reverse('create_post', args=[self.community.id]), data=form_data)
        
        # Check if the post was created successfully
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Post.objects.filter(communit_id=self.community, author=self.test_user1).exists())
    

    def test_post_request_invalid_form(self):
        # Test POST request with invalid form data
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        
        form_data = {
            'title': 'Test Title',  # This is a required field
        }
        response = self.client.post(reverse('create_post', kwargs={'community_id': self.community.id}), data=form_data)
        
        # Check if the post was not created successfully
        self.assertNotEqual(response.status_code, 200)
    
    
