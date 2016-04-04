from django.contrib import admin
from .models import ContactForm


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')

    class Meta:
        model = ContactForm

admin.site.register(ContactForm, ContactFormAdmin)
