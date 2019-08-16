from service import models
from . import serializers
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib import auth


class AccountViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['POST'])
    def signup(self, request: 'Response') -> 'Response':
        serializer = serializers.SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        auth.login(request, user)

        return Response([True], status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_authenticated:
            auth.logout(request)

        username, password = serializer.validated_data['username'], serializer.validated_data['password']
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)

        return Response([True], status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if not request.user.is_authenticated:
            response = [False]
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = request.user
            auth.logout(request)
            response = [True]
        return Response(response, status=status.HTTP_200_OK)


class ShipViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user
        if user.is_anonymous:
            return Response([False], status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_superuser:
            queryset = models.Ship.objects.filter(owner=user)
        else:
            queryset = models.Ship.objects.all()
        serializer = serializers.ShipSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user
        if user.is_anonymous:
            return Response([False], status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_superuser:
            queryset = models.Ship.objects.filter(owner=user)
        else:
            queryset = models.Ship.objects.all()
        ship = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ShipSerializer(ship)
        ship_history_qs = models.LatLngHistory.objects.filter(ship=ship)
        ship_history_serializer = serializers.LatLngHistorySerializer(ship_history_qs, many=True)
        resp = serializer.data
        resp['history'] = ship_history_serializer.data
        return Response(resp)
