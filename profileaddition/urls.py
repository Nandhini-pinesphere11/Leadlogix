from django.urls import path
from . import views


urlpatterns = [
    path('profile_add/',views.profile_add,name='profile_add'),
    path('user-profile/', views.show_profile, name='show_profile'),

]