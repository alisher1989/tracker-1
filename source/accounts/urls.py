from django.urls import path
from accounts.views import logout_view, login_view, register_view, \
    user_activate_view, UserDetailView, UserChangeView, UserChangePasswordView, UsersListView, password_reset_email_view, PasswordResetFormView

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('activate/<token>/', user_activate_view, name='user_activate'),
    path('profile/<pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<pk>/edit', UserChangeView.as_view(), name='user_update'),
    path('profile/<pk>/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('reset-password/', password_reset_email_view, name='password_reset_email'),
    path('reset-password/<token>/', PasswordResetFormView.as_view(), name='password_reset_form')
]


app_name = 'accounts'