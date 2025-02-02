from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import firestore

# Create your views here.

class Register(APIView):
  def post(self, request):
      try:    
        db = firestore.client()
        # uid = request.data['uid']
        user_ref = db.collection('user')
        user_ref.add({
            'username': request.data["username"], 
            'email': request.data["email"],
            'password': request.data["password"],
        })
      except KeyError:
          return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      return Response({'message': 'New user has been registered successufully.'}, status=status.HTTP_202_ACCEPTED)

class Login(APIView):
    def post(self, request):
        pass

