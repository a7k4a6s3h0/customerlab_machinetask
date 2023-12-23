from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
import rest_framework
from rest_framework import generics, status
from app.models import Account, Destination
from app.serializers import DestinationSerializer
from . serializers import *
import requests

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationByAccountView(generics.ListAPIView):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        return Destination.objects.filter(account__account_id=account_id)

class Add_Destination(generics.CreateAPIView):
    serializer_class = AddDestinationSerializer
    def post(self, request):
        account_id = self.request.query_params.get('account_id')
        try:
            account = Account.objects.get(account_id = account_id)
            serializer = AddDestinationSerializer(data=request.data, context={'acc_object': account})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': status.HTTP_200_OK,'msg':"Destination add sucessfully", 'details': serializer.data})
            
        except Account.DoesNotExist as e:
            return JsonResponse({"error": "Invalid account id."}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateDestination(generics.UpdateAPIView):
    serializer_class = UpdateDestinationSerializer
    def put(self, request, *args, **kwargs):

        acc_id = self.request.query_params.get('acc_id')
        des_id = self.request.query_params.get('des_id')

        destinations = Destination.objects.filter(account=acc_id)
        for curr_des in destinations:
            if curr_des.id == int(des_id):
                print(curr_des.url)
                serializer = self.serializer_class(curr_des, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status= status.HTTP_200_OK)
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        raise serializers.ValidationError("You can only edit your own account")
            
    
class deleteDestination(generics.DestroyAPIView):
    serializer_class = DeleteDestinationSerializer
    def delete(self, request, *args, **kwargs):
        try:
            destination = Destination.objects.get(id=request.data.get('id'))
            destination.delete()
            return JsonResponse({"message":"Successfully deleted the destination"}, status=status.HTTP_204_NO_CONTENT)
        except Destination.DoesNotExist as e:

            return JsonResponse({"error":str(e), "status":status.HTTP_204_NO_CONTENT})
            

class IncomingDataView(generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        app_secret_token = request.headers.get('CL-X-TOKEN')

        if not app_secret_token:
            return JsonResponse({'error': 'Unauthenticated'}, status=401)

        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Invalid App Secret Token'}, status=401)

        destinations = Destination.objects.filter(account=account)
        
        if not destinations:
            return JsonResponse({'error': 'No Destinations Found For This User'}, status=404)

        for destination in destinations:
            if destination.http_method == 'GET':
                if not request.content_type == 'application/json':
                    return JsonResponse({'error': 'Invalid Data'}, status=400)
            else:

                headers = destination.headers
                method = destination.http_method.lower()
                url = destination.url

                if method == 'post':
                    response = requests.post(url, headers=headers, json=data)
                elif method == 'put':
                    response = requests.put(url, headers=headers, json=data)
                # Add other HTTP methods as needed

                # Check the response status and handle accordingly
                if response.status_code != 200:
                    return JsonResponse({'error': f'Data sending failed. Status code: {response.status_code}'}, status=response.status_code)

                return JsonResponse({'success': 'Data sent successfully'})    
                
        return JsonResponse({'success': 'Data sent successfully'})        
