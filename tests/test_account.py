import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient


pytestmark = [
    pytest.mark.django_db,
]

@pytest.fixture
def user_of_ivan():
    return User.objects.create_user(username='ivan', password='xa6eiQuoo3')


class SignUpTest:
    def test_201(self, client):
        # register anonymous user
        url = reverse('account-signup')
        data = {
            'username': 'username',
            'password': 'xa6eiQuoo3',
            'email': 'username@test.test',
            'kind': 'teacher',
        }
        response = client.post(url, data=data)

        assert response.status_code == 201
        assert response.data

    def test_400(self, client, user_of_ivan):
        # register ivan, who already was registered
        url = reverse('account-signup')

        data = {
            'username': 'ivan',
            'password': 'xa6eiQuoo3',
            'email': 'ivan@test.test',
            'kind': 'teacher',
        }
        response = client.post(url, data=data)

        assert response.status_code == 400
        assert response.data


class LoginTest:
    def test_200(self, client, user_of_ivan):
        # login ivan, who already was registered
        url = reverse('account-login')

        data = {
            'username': 'ivan',
            'password': 'xa6eiQuoo3',
        }
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.data

    def test_401(self, client):
        # login anonymous user
        url = reverse('account-login')

        data = {
            'username': 'username',
            'password': 'xa6eiQuoo3',
        }
        response = client.post(url, data=data)

        assert response.status_code == 401
        assert response.data


class LogoutTest:
    def test_200(self, client, user_of_ivan):
        # logout ivan, who already was registered and login
        LoginTest.test_200(LoginTest(), client=client, user_of_ivan=user_of_ivan)
        url = reverse('account-logout')
        response = client.post(url)
        assert response.status_code == 200
        assert response.data

    def test_401(self, client):
        # logout anonymous user
        url = reverse('account-logout')
        response = client.post(url)

        assert response.status_code == 401
        assert response.data
