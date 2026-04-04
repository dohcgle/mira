from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import LoanApplication

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token['username'] = user.username
        # Userning birinchi guruhini 'role' qilib olamiz
        group = user.groups.first()
        token['role'] = group.name if group else 'unknown'
        return token

class LoanApplicationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = LoanApplication
        fields = ['id', 'data', 'status', 'created_at', 'updated_at', 'created_by_name']
        read_only_fields = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']
