from django.urls import path, include
from . import views
from allauth.account.views import SignupView
from .views import AddAuthorView
from django.contrib.auth.views import LoginView, LogoutView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from .views import UserProfileUpdateView




urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('search/', views.news_search, name='news_search'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('create/', views.news_create, name='news_create'),
    path('<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('<int:pk>/delete/', views.news_delete, name='news_delete'),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('add_author/', AddAuthorView.as_view(), name='add_author'),
    path('login/', LoginView.as_view(template_name='login.html'), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
    path('signup/', SignupView.as_view(template_name='signup.html'), name='account_signup'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
    path('google/login/', OAuth2LoginView.as_view(adapter=GoogleOAuth2Adapter), name='google_login'),
    path('google/callback/', OAuth2CallbackView.as_view(adapter=GoogleOAuth2Adapter), name='google_callback'),
]
