from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

# Serializer for reading and updating user data
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        # Custom update logic if needed (password update or other fields)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash new password if it is provided
        return super().update(instance, validated_data)





