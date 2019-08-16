from rest_framework import routers
from . import views


router = routers.DefaultRouter()


router.register('account', views.AccountViewSet, 'account')
router.register('ships', views.ShipViewSet, 'ships')


urlpatterns = router.urls
