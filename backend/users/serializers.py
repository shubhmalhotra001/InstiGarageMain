from rest_framework import serializers
from .models import User
  
# serialized the user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password','phone','wallet']
        extra_kwargs = {
            'password': {'write_only': True} # password will not be returned in the user details back to the user
        }

    def create(self, validated_data): # called when creating a new user
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) # Convert the password from plain text to hash
        instance.save()
        return instance
