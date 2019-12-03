from django.urls import path, include
from rest_framework import routers
from api.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]