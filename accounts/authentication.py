from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomToken, User

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').replace('Token ', '')
        
        if not token:
            return None 
        try:
            custom_token = CustomToken.objects.get(key=token)
            
            if custom_token.user_type == 'teacher':
                return (custom_token.teacher, custom_token)
            elif custom_token.user_type == 'student':
                return (custom_token.student, custom_token)
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')  
        return None
