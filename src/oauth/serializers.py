from rest_framework import serializers
from models import Users, Emails

class homeSerializer(serializers.Serializer):
    sign_in_url = serializers.URLField()

class tokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    username = serializers.CharField()


class mailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Emails
            fields = (
            'id',
            'username',
            'title',
            'date',
            'start_time',
            'end_time',
            )

class UserSerializer(serializers.ModelSerializer):
    mails = mailSerializer(many=True)
    class Meta:
        model=Users
        fields = (
        'id',
        'email',
        'mails',
        )

