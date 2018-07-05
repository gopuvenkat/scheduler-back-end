from rest_framework import serializers

class homeSerializer(serializers.Serializer):
    sign_in_url = serializers.URLField()
