from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag

admin.site.register(Project)  # Get the table Project into our admin view
admin.site.register(Review)  # Get the table Project into our admin view
admin.site.register(Tag)  # Get the table Project into our admin view
