from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from typing import Dict, Any 

class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    
    @classmethod
    def get_token(cls, user) -> Dict[str, Any]:# type: ignore
        token = super().get_token(user)
        token['username'] = user.username
        return token # type: ignore
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    