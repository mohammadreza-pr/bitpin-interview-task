from rest_framework import serializers
from .models import Content, Rate

class CreateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['title', 'text']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ContentSerializer(serializers.ModelSerializer):

    user_rate = serializers.SerializerMethodField()
    class Meta:
        model = Content
        fields = ['id', 'title', 'total_votes', 'average_score', 'user', 'user_rate']
    
    
    def get_user_rate(self, obj):
        user = self.context['request'].user  
        rating = Rate.objects.filter(user=user, post=obj).first()
        return rating.score if rating else None
    
class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['score', 'post']
    
    


