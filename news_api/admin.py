from django.contrib import admin

from news_api.models import News, Comment, Upvote

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Upvote)