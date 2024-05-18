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
            'is_private': False,  # Assuming it's not private for this test
            'picture': SimpleUploadedFile(
                'mock_image.png',
                image_io.read()
            )  # You can provide a mock image file if needed
        }
        response = self.client.post(reverse('community-create'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Assuming you're rendering a page upon successful form submission
        self.assertTrue(Community.objects.filter(name='Test Community').exists())


