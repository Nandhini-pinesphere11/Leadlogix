from django.contrib import admin
from .models import Contact, Employee, ProductType, CustomizedEmail, Attachment, BrandMailer, BrandAttachment,ComposeMessage,ComposeAttachment

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'phone', 'email','state','date_of_enquiry','company_name','customer_confidence')
    list_filter = ('first_name', 'email')
    search_fields = ('first_name', 'email')

admin.site.register(Employee)
admin.site.register(ProductType)
admin.site.register(CustomizedEmail)
admin.site.register(Attachment)
admin.site.register(BrandMailer)
admin.site.register(BrandAttachment)
admin.site.register(ComposeMessage)
admin.site.register(ComposeAttachment)
