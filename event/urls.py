from django.urls import path
from . import views


urlpatterns = [
    path('CreateEvent/',views.Create_event,name="Create_event"),
    path('event_dashboard/<str:username>/<int:event_id>/', views.event_dashboard, name='event_dashboard'),
    path('event_reports/<str:username>/<int:event_id>/', views.event_reports, name='event_reports'),
    path('fetch_datas/<str:username>/<int:event_id>/',views.fetch_datas,name='fetch_datas'),
    path('event_form/Strings/<int:event_id>/', views.event_form, name='event_form'),
    path('get_customer_confidence_datas/<int:event_id>/',views.get_customer_confidence_datas, name='get_customer_confidence_datas'),
    path('get_contact_counts/<int:event_id>/',views.get_contact_counts, name='get_contact_counts'),
    path('get_engage_datas/<int:event_id>/',views.get_engage_datas,name='get_engage_datas'),
    path('remove_ename/', views.remove_ename, name='remove_ename'),
    path('signin/',views.login_view,name="signin"),
    path('get-products/', views.get_products, name='get_products'), 
    path('event_compose/', views.event_compose_message, name='event_compose_message'),
   
] 

