from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema
from . import views

app_name = 'users'

jwt_urlpatterns = [

    # To organize these views by tags in Spectacular, we used the extend_schema decorator.

    path(
        'login/',
        extend_schema(tags=['Simple JWT Authentication'])(TokenObtainPairView).as_view(),
        name='token_obtain_pair'
    ),
    path(
        'refresh/',
        extend_schema(tags=['Simple JWT Authentication'])(TokenRefreshView).as_view(),
        name='token_refresh'
    ),

]

app_urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile')
]

urlpatterns: list = jwt_urlpatterns + app_urlpatterns
