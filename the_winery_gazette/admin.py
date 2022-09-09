from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """ admin display for the gazette posts """

    list_display = ('title', 'slug', 'author', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ admin display for the gazette comments """

    list_display = ('author', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('author', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """ function to approve comments for display """

        queryset.update(active=True)


admin.site.register(Post, PostAdmin)
