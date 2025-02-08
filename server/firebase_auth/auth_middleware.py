from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth

def firebase_auth_required(view_func, *arg, **karg):
    @wraps(view_func)
    def _wraped_view(request, *arg, **karg):
        id_token = request.headers.get('Authorization')
        
        if not id_token:
            return Response({ 'success': False, 'message': 'Unauthorized' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.user = decoded_token
            view_func(request, *arg, **karg)
        except Exception as e:
            pass
    
    return _wraped_view