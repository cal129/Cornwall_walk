from django.contrib import admin
from post_walk.models import postwalk
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(postwalk)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'authorised')
    search_fields = ['title']
    list_filter = ('authorised',)
    prepopulated_fields = {'slug': ('title',)}
