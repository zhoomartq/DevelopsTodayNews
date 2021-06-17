from rest_framework import serializers
from .models import *

class NewsSerializer(serializers.ModelSerializer):


    class Meta:
        model = News
        fields = ('id', 'title', )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.profile_producer
        product = News.objects.create(author=user, **validated_data)

        return product



    def to_representation(self, instance):
        representation = super(NewsSerializer, self).to_representation(instance)
        action = self.context.get('action')
        comments = CommentSerializer(instance.reviews.all(), many=True).data
        upvotes = UpvoteSerializer(instance.likes.filter(like=True), many=True).data
        representation['author'] = instance.author.email
        if action == 'list':
            representation['comments'] = len(comments)
            representation['upvotes'] = len(upvotes)
        if action == 'retrieve':
            representation['reviews'] = CommentSerializer(instance.comments.all(), many=True).data
            representation['likes'] = UpvoteSerializer(instance.upvotes.filter(upvote=True), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'news', 'body', )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.CustomUser
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation

class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ('user', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation

