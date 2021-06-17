from django.contrib.auth import get_user_model
from django.db import models
from user.models import CustomUser

User = get_user_model()

class News(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    link = models.TextField()


    def __str__(self):
        return f'{self.title}--{self.created}'

    class Meta:
        ordering = ('created',)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}--{self.created}--{self.body[0:10]}'

    class Meta:
        ordering = ('created', )

class Upvote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    amount_of_upvotes = models.AutoField(primary_key=True)
    upvote = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} Upvoted this news--> {self.news}'
