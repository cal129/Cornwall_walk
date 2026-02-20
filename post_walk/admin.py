from django.contrib import admin
from post_walk.models import postwalk, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(postwalk)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'authorised')
    search_fields = ['title']
    list_filter = ('authorised',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'walk', 'created_date', 'authorised')
    list_filter = ('authorised', 'created_date')
    search_fields = ['user__username', 'walk__title', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(authorised=True)
    approve_comments.short_description = 'Approve selected comments'