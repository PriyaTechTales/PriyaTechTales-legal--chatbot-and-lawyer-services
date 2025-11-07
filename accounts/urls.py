from django.urls import path
from .views import SimpleLoginView, logout_view, signup, post_login_redirect, profile

urlpatterns = [
    path('login/', SimpleLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('post-login/', post_login_redirect, name='post_login_redirect'),
    path('profile/', profile, name='profile'),
]
