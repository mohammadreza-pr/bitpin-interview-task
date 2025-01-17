from rest_framework import routers
from .views import ContentViewset

router = routers.DefaultRouter()

router.register('', ContentViewset, basename='content')

urlpatterns = router.urls