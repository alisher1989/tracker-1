from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import ProjectViewSet, TaskViewSet, LogoutView

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)



app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='obtain_token_auth'),
    path('logout/', LogoutView.as_view(), name='delete_auth-token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]