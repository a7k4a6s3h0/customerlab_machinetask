import django.db
from rest_framework import serializers
from .models import Account, Destination

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class Add_AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('email', 'account_id', 'account_name', 'app_secret_token', 'website')  
        read_only_fields = ('account_id', 'app_secret_token')  


class UpdateAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('email', 'account_name', 'website')  # Fields that are allowed to be updated

    # Override the update method on the ModelViewSet so we can check if an account with the same email already exists in the database before saving
        
    def update(self, instance, validated_data):
        if instance.account_id == self.context.get('account_id'):
            instance.email = validated_data.get('email', instance.email)
            instance.account_name = validated_data.get('account_name', instance.account_name)
            instance.website = validated_data.get('website', instance.website)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'error':'No Account Found With This ID'})

class DeleteAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model=Account
        fields=( 'account_id',)
    