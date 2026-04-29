from django.urls import path
from . import views

# URL patterns for the accounts app
# Each path maps a URL to a view function
urlpatterns = [
    path('', views.home, name='home'),                                          # Landing page
    path('login/', views.login_view, name='login'),                             # Login page
    path('register/', views.register_view, name='register'),                    # Register page
    path('logout/', views.logout_view, name='logout'),                          # Logs user out
    path('dashboard/', views.dashboard, name='dashboard'),                      # Dashboard (login required)
    path('forgot-password/', views.forgot_password, name='forgot_password'),    # Forgot password page
]
