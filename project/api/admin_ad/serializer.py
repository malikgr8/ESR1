from rest_framework import serializers
from project.feed.models.admin_ad import AdminAd


class AdminAdSerializer(serializers.ModelSerializer):

    CATEGORY_FREQUENCY = {
        'S': 100,
        'G': 250,
        'D': 500
    }
    frequency = serializers.SerializerMethodField()

    class Meta:
        model = AdminAd
        fields = [
            'title', 
            'category', 
            'expiry', 
            'deeplink', 
            'is_active',
            'frequency'
        ]
    
    def get_frequency(self, admin_ad):
        return self.CATEGORY_FREQUENCY.get(admin_ad.category)