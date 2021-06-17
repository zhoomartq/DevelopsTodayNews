from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from news_api.models import News, Upvote, Comment
from news_api.serializers import NewsSerializer, CommentSerializer, UpvoteSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        news = self.get_object()
        obj, created = Upvote.objects.get_or_create(user=request.user.profile_customer, news=news)
        if not created:
            obj.upvote = not obj.upvote
            obj.save()
        upvoted_or_voted = 'upvoted' if obj.like else 'voted'
        return Response('Successfully {} product'.format(upvoted_or_voted), status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpvoteCreateListView(generics.ListAPIView):
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer

    def get_queryset(self):
        qs = self.request.user.profile_customer
        queryset = Upvote.objects.filter(user=qs, upvote=True)
        return queryset
