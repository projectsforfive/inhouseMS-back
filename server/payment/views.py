from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import firestore
import uuid

# Create your views here.

class NewPay(APIView):
  def post(self, request):
    data = request.data.copy()
    uid = data.get('uid')
    data['id']= str(uuid.uuid4())
    if not data:
      return Response({'message': 'Data is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
      db = firestore.client()
      doc_ref = db.collection('payment').document(uid)
      pay_info = doc_ref.get()
      if pay_info.exists:
        existing_outcomes = pay_info.to_dict().get(uid)
        print(existing_outcomes)
        doc_ref.update({'scores': firestore.ArrayUnion([data])})
        print('scores updated')
      else:
      # If it doesn't exist, create a new document with the lecture
        doc_ref.set({'scores': [data]})  
        print('scores created')
    except KeyError:
        return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'message': 'New payment has been registered successufully.'}, status=status.HTTP_202_ACCEPTED)
  
class GetPayments(APIView):
  def get(self, request, uid):
    try:
      print(uid)
      db = firestore.client()
      doc_ref = db.collection('payment').document(uid)
      payments = doc_ref.get()
      print(payments)
      if payments.exists:
        existing_outcomes = payments.to_dict().get('scores')
      #   # print(existing_outcomes)
        return Response({'data': existing_outcomes}, status=status.HTTP_200_OK)
      else:
        return Response({'message': 'No payment found.', 'data': None}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class GetOnePayment(APIView):
  def get(self, request, uid, id):
    print(uid,id)
    try:
      db = firestore.client()
      doc_ref = db.collection('payment').document(uid)
      outcomes = doc_ref.get()
      if outcomes.exists:
        # Get outcomes based on uid
        existing_outcomes_dict = outcomes.to_dict().get('scores')
        print(existing_outcomes_dict)
        data = [item for item in existing_outcomes_dict if item.get('id') == id]
        print(data)
        if data:
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No outcomes found.', 'data': None}, status=status.HTTP_404_NOT_FOUND)
      else:
        return Response({'message': 'No outcomes found.', 'data': None}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def put(self, request, uid, id):
    data = request.data.copy()
    data.update({'id': id})
    try:
      db = firestore.client()
      print(data)
      doc_ref = db.collection('payment').document(uid).get()
      origin_outcomes = doc_ref.to_dict().get('scores')
      updated_outcomes = [
          data if origin_outcome['id'] == data['id'] else origin_outcome
          for origin_outcome in origin_outcomes
      ]
      db.collection('payment').document(uid).update({'scores': updated_outcomes})
      return Response({'message': 'payment updated successfully.'}, status=status.HTTP_202_ACCEPTED)
    except KeyError:
      return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def delete(self, request, uid, id):
    try:
      db = firestore.client()
      doc_ref = db.collection('payment').document(uid)
      outcomes = doc_ref.get()
      if outcomes.exists:
        # Get outcomes based on uid
        existing_outcomes_dict = outcomes.to_dict().get('scores')
        data = [item for item in existing_outcomes_dict if item.get('id') == id]
        print(data)
        if data:
          doc_ref.update({'scores': firestore.ArrayRemove([data[0]])})
          return Response({'message': 'payment deleted successfully.'}, status=status.HTTP_202_ACCEPTED)
        else:
          return Response({'message': 'No payment found.', 'data': None}, status=status.HTTP_404_NOT_FOUND)
      else:
        return Response({'message': 'No payment found.', 'data': None}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
