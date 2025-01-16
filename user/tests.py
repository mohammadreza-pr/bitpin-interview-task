from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
        }

       
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password'],  
        )

    def test_signup_success(self):
        """Test successful signup"""
        response = self.client.post('/api/user/signup/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], 'newuser')

    def test_signup_missing_fields(self):
        """Test signup with missing required fields"""
        response = self.client.post('/api/user/signup/', {
            'username': 'newuser',
        })  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_token_obtain_success(self):
        """Test obtaining token with valid credentials"""
        response = self.client.post('/api/user/token/', {
            'username': self.user_data['username'],
            'password': self.user_data['password'],  
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  
        self.assertIn('refresh', response.data)  

    def test_token_obtain_invalid_credentials(self):
        """Test obtaining token with invalid credentials"""
        response = self.client.post('/api/user/token/', {
            'username': self.user_data['username'],
            'password': 'wrongpassword',  
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        """Test refreshing token with a valid refresh token"""
        
        token_response = self.client.post('/api/user/token/', {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)

        refresh_token = token_response.data['refresh']  

        response = self.client.post('/api/user/token/refresh/', {
            'refresh': refresh_token,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_refresh_invalid_token(self):
        """Test refreshing token with an invalid refresh token"""
        response = self.client.post('/api/user/token/refresh/', {
            'refresh': 'invalid_refresh_token',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
