from tailorscoop import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('today/', views.today_story, name='today'),
    path('unsubscribe_confirm/<str:hashed_email>/', views.unsubscribe_confirm, name='unsubscribe_confirm'),
    path('unsubscribe/<str:hashed_email>/', views.unsubscribe, name='unsubscribe'),   
    path('log_click/<str:encoded_url>/<str:hashed_email>/', views.log_click_and_redirect, name='log_click_and_redirect'),
]