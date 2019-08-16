import pytest
from django.conf import settings
import pandas as pd
import datetime
from os import listdir
from django.contrib.auth.models import User
from service import models
from django.urls import reverse
from api_v1 import serializers

from rest_framework.test import APIClient
import pytz

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def user_of_ivan():
    return User.objects.create_user(username='ivan', password='xa6eiQuoo3')


@pytest.fixture
def superuser_of_timofey():
    user = User.objects.create_user(username='timofey', password='xa6eiQuoo3')
    user.is_superuser = True

    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(client, user_of_ivan):
    client.force_authenticate(user=user_of_ivan)
    return client


@pytest.fixture
def super_user(client, superuser_of_timofey):
    client.force_authenticate(user=superuser_of_timofey)
    return client


@pytest.fixture
def ships():
    way = settings.MEDIA_ROOT + "/files/"

    current_files = listdir(way)
    try:
        current_files.pop(current_files.index('.DS_Store'))
    except:
        pass

    new_files = current_files
    for file_name in new_files:
        df = pd.read_excel(way + file_name)
        for i in df.values:
            code = i[0]
            dt = datetime.datetime.combine(datetime.datetime.date(i[1]), i[2], tzinfo=pytz.UTC)
            lat = i[3]
            lng = i[4]
            name = i[5]

            if not models.Ship.objects.filter(code=code):
                models.Ship.objects.create(name=name, code=code)
            ship = models.Ship.objects.get(code=code)
            models.LatLngHistory.objects.create(
                dt=dt,
                lat=lat,
                lng=lng,
                ship=ship
            )

    return models.Ship.objects.all()


@pytest.fixture
def ships_with_owner(ships, user_of_ivan):
    for i in ships[:5]:
        i.owner = user_of_ivan
        i.save()
    return models.Ship.objects.all()


# noinspection PyMethodMayBeStatic
class ShipViewSetTest:
    class ShipViewSetListTest:
        def test_anon_user_ships(self, client):
            url = reverse('ships-list')

            response = client.get(url)
            assert response.status_code == 401

        def test_ship_user_ships(self, user, ships_with_owner, user_of_ivan):
            url = reverse('ships-list')
            response = user.get(url)

            assert response.data == serializers.ShipSerializer(ships_with_owner.filter(owner=user_of_ivan), many=True).data

        def test_ship_super_user_ships(self, super_user, ships):
            url = reverse('ships-list')
            response = super_user.get(url)

            assert response.data == serializers.ShipSerializer(ships, many=True).data


    class ShipViewSetRetrieveTest:
        def test_anon_user_ships(self, client, ships):
            def test_check_ship(code):
                url = reverse('ships-detail', args=[code])
                response = client.get(url)
                assert response.status_code == 401

            codes = ships.values_list("code", flat=True)

            for code in codes:
                test_check_ship(code)

        def test_ship_user_ships(self, user, ships_with_owner, user_of_ivan):
            def test_check_ship(code):
                url = reverse('ships-detail', args=[code])
                owner_codes = ships_with_owner.filter(owner=user_of_ivan).values_list("code", flat=True)
                response = user.get(url)
                if code not in owner_codes:
                    assert response.status_code == 404
                else:
                    ship = ships_with_owner.get(code=code)
                    data = serializers.ShipSerializer(ship).data

                    history_data = serializers.LatLngHistorySerializer(models.LatLngHistory.objects.filter(ship=ship),
                                                                       many=True).data
                    data['history'] = history_data
                    assert response.data == data

            codes = ships_with_owner.values_list("code", flat=True)

            for code in codes:
                test_check_ship(code)

        def test_ship_super_user_ships(self, super_user, ships):
            def test_check_ship(code):
                url = reverse('ships-detail', args=[code])
                response = super_user.get(url)
                ship = ships.get(code=code)
                data = serializers.ShipSerializer(ship).data

                history_data = serializers.LatLngHistorySerializer(models.LatLngHistory.objects.filter(ship=ship),
                                                                   many=True).data
                data['history'] = history_data
                assert response.data == data

            codes = ships.values_list("code", flat=True)

            for code in codes:
                test_check_ship(code)
