"""tickers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from posixpath import basename
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#from django.conf.urls.static import static
# from tick_app.views import UserViewSet
# from rest_framework.routers import DefaultRouter

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     # @classmethod
#     # def get_token(cls, user):
#     #     token = super().get_token(user)

#     #     # Add custom claims
#     #     token['role'] = "Admin" if user.is_superuser else "User"
#     #     # ...

#     #     return token
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)

#         # Add extra responses here
#         data['role'] = "Admin" if self.user.is_superuser else "User"
#         return data

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/", include("tick_app.urls")),
    # path("api-auth/", include('rest_framework.urls')),
    # path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# router = DefaultRouter()
# router.register('user', UserViewSet, basename='user')

# urlpatterns += router.urls
