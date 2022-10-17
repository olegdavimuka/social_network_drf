"""social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from posts import views as post_views
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from users import views as user_views

router = routers.DefaultRouter()
router.register(r"users", user_views.UserViewSet)
router.register(r"posts", post_views.PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/signup/", user_views.SignUpView.as_view(), name="signup"),
    path(
        "api/user-activity/<int:pk>",
        user_views.UserActivity.as_view(),
        name="user_activity",
    ),
    path(
        "api/posts/<int:pk>/like/", post_views.PostLikeView.as_view(), name="like_post"
    ),
    path(
        "api/posts/<int:pk>/unlike/",
        post_views.PostUnlikeView.as_view(),
        name="unlike_post",
    ),
    path("api/analytics/", post_views.AnalyticsView.as_view(), name="analytics"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
