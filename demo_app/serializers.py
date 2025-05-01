#mapping the request with model and viceversa ->serialiser

from django.forms import ValidationError
from rest_framework import serializers
from .models import register,Profile

from django.contrib.auth.hashers import make_password

class registerSerializer(serializers.ModelSerializer):
   
    password = serializers.CharField(write_only=True)

    class Meta:
        model = register
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
       
        password = validated_data.pop('password')
        user = register(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'birth_date','gender','blood_group']

    def create(self, validated_data):
        request = self.context.get('request')  # Get request from context
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be logged in.")
        
        validated_data['user'] = request.user  # Set the user before saving
        return super().create(validated_data)


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id', 'username', 'age', 'gender', 'created_at', 'updated_at']
#         # read_only_fields = ['id', 'created_at', 'updated_at']  # These fields should not be manually set
        






# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')
#         print(f"Username: {username}, Password: {password}") 

#         # Try to get the user from the custom Register model
#         try:
#             user = register.objects.get(username=username)
#         except register.DoesNotExist:
#             raise ValidationError("Invalid username or password")

#         # Check if the password is correct
#         if not user.check_password(password):
#             raise ValidationError("Invalid username or password")

#         return {'user': user} 

