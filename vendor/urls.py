from django.urls import path
from . import views


urlpatterns = [
    path('vendor/', views.vendor, name='vendor'),
    path('forms/<str:username>/', views.forms, name='forms'),
    path('department/', views.department, name='department'),
    path('remove_dname/', views.remove_dname, name='remove_dname'),
    path('reports/',views.reports, name='reports'),

    path('fetch/', views.fetch, name='fetch'),
 
]

