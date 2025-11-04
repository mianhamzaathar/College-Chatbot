from django.contrib import admin
from .models import Library

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'available_copies')  # Add more fields if needed
    search_fields = ('title', 'author')  # Optional: allow searching by title or author
    list_filter = ('publication_date',)  # Optional: filter by publication date
