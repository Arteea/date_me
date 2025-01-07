"""
URL configuration for date_me project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# Импорты
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from users.tokens import CustomTokenObtainPairView
from users.views import UserProfileView,SelectGenderView,EnterNameSurnameView,EnterContactInfoView,ConfirmEmailView


# Схема OpenAPI для DRF
schema_view = yasg_get_schema_view(
    openapi.Info(
        title="Date_me",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('rest_framework.urls')),
    path('', include('users.urls')),
    path('api/token/accounts/profile/<int:user_id>/',UserProfileView.as_view({'get':'profile','put':'profile'})),
    path('api/token/accounts/create_profile/',UserProfileView.as_view({'post':'create_profile'})),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('',include('dialogs.urls')),
    path('',include('compatability.urls')),
    path('select_gender/',SelectGenderView.as_view({'post':'select_gender'})),
    path('enter_name_surname/',EnterNameSurnameView.as_view({'post':'enter_name_surname'})),
    path('enter_contact_info/',EnterContactInfoView.as_view({'post':'enter_contact_info'})),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('confirm_email/<str:token>/', ConfirmEmailView.as_view()),
]
