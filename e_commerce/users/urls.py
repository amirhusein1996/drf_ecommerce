from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema
from . import views

app_name = 'users'

jwt_urlpatterns = [

    # To organize these views by tags in Spectacular, we used the extend_schema decorator.

    path(
        'token/',
        extend_schema(tags=['Simple JWT Authentication'])(TokenObtainPairView).as_view(),
        name='token_obtain_pair'
    ),
    path(
        'refresh/',
        extend_schema(tags=['Simple JWT Authentication'])(TokenRefreshView).as_view(),
        name='token_refresh'
    ),
    path(
        'verify/',
        extend_schema(tags=['Simple JWT Authentication'])(TokenVerifyView).as_view(),
        name='token_verify'
    ),
]

app_urlpatterns = [

]

urlpatterns: list = jwt_urlpatterns + app_urlpatterns
