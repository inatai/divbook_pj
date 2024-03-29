from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('profile/edit', views.ProfileEditView.as_view(), name='profile_edit'),
    # path('signup/', views.SignupView.as_view(), name='account_signup'),
]