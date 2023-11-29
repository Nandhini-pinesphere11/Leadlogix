from django.urls import path
from . import views


urlpatterns = [
    path('exform/',views.exform,name='exform'),
    path('reports_excust/',views.ex_customer_reports,name='reports_excust'),
    path('edit_excustomer/<int:pk>/', views.edit_excustomer, name='edit_excustomer'),
    path('excustomer/view/<int:excustomer_id>/', views.view_excustomer, name='view_excustomer'),
    path('excustomer_compose/', views.excustomer_compose_message, name='excustomer_compose_message'),

]
