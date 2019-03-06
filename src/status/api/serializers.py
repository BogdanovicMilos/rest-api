from rest_framework import serializers
from status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['user', 'content', 'image']

    # def validate_content(self, value):
    #     if len(value) > 10000:
    #         raise serializers.ValidationError('Too long')
    #     return value

    def validate(salf, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if content is None and image is None:
            raise serializers.ValidationError('Content or image is required')
        return data
