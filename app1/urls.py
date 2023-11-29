from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('index1/', views.index1, name='index1'),
    path('manageforms/', views.manageforms, name='manageforms'),
    path('get_customer_confidence_data/', views.get_customer_confidence_data, name='get_customer_confidence_data'),
    path('get_employee_counts/',views.get_employee_counts, name='get_employee_counts'),
    path('get_contact_count/', views.get_contact_count, name='get_contact_count'),
    path('get_engage_data/',views.get_engage_data, name = 'get_engage_data'),

    path('products_add/',views.products_add,name="product_list"),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),


    path('employee_list/', views.employee_list, name='employee_list'),
    path('delete_employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),

    path('products_lists/', views.product_lists, name="product_lists"),
    path('delete_attachments/',views.delete_attachments, name="delete_attachments"),

    path('get_unread_notifications/', views.get_unread_notifications, name='get_unread_notifications'),
    path('clear_notifications/', csrf_exempt(views.clear_notifications), name='clear_notifications'),

    #mainform
    path('mainform/Strings/', views.mainform, name='mainform'),
    path('get-product/', views.get_product, name='get_product'),
    path('brand/', views.brand, name='brand'),

    path('delete-attachment/<int:attachment_id>/', views.delete_attachment, name='delete-attachment'),

    path('get_existing_employee/',views.get_existing_employee,name='get_existing_employee'),
    path('compose/', views.compose_message, name='compose_message'),
    path('get_customized_email/', views.get_customized_email, name='get_customized_email'),

]
 
