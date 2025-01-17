from rest_framework import routers
from .views import ContentViewset, RateViewset

router = routers.DefaultRouter()

router.register('', ContentViewset, basename='content')
router.register('rate', RateViewset, basename= 'rate')

urlpatterns = router.urls