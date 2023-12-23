import django.db
from rest_framework import serializers
from app.models import Destination


class AddDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ('url', 'http_method', 'headers')

    def create(self, validated_data):
        
        curr_accobj = self.context.get('acc_object')
        validated_data['account'] = curr_accobj
        return super().create(validated_data)    
    
class UpdateDestinationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Destination
        fields = ('url', 'http_method', 'headers')
        extra_kwargs = {
            'url':{'required': False},
            'http_method': {'required': False},
            'headers': {'required': False},
        }


    def update(self, instance, validated_data):
        print("enter")
        instance.url = validated_data.get('url', instance.url)
        instance.http_method = validated_data.get('http_method', instance.http_method)
        instance.headers = validated_data.get('headers', instance.headers)
        instance.save()
        return instance

class DeleteDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ('id', )
                
