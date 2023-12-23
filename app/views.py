
from django.shortcuts import render

# Create your views here.


from rest_framework import generics, status
from rest_framework.response import Response
from .models import Account, Destination
from django.http import JsonResponse
from .serializers import *


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer



#........................... CURD Operation For Account ........................
    
class RegisterAccount(generics.CreateAPIView):
    serializer_class = Add_AccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = Add_AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':200,
                'msg':'Sucessfully registerd..',
                'Account_Details': serializer.data
            })
        return Response({
            'status':400,
            'msg':serializer.errors
        }
        )

class UpdateAccount(generics.UpdateAPIView):
    serializer_class = UpdateAccountSerializer
    lookup_field = 'account_id'

    def put(self, request, *args, **kwargs):   

        account_id = self.request.query_params.get('account_id')
        print(account_id, "id......")

        try:
            user = Account.objects.get(account_id=account_id)
            print(user, "curr_user....")
            serializer = self.serializer_class(user, data=request.data, context={'account_id': account_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Status": "Success", "Message":"User has been updated successfully"}, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist as e:
            return Response({
                'status':400,
                'error':str(e)
            })    
        
class DeleteAccount(generics.DestroyAPIView):
    serializer_class = DeleteAccountSerializer

    def delete(self, request, *args, **kwargs):
        # account_id = self.request.query_params.get('account_id')
        app_secret_token = request.headers.get('CL-X-TOKEN')

        if not app_secret_token:
            return JsonResponse({'error': 'Unauthenticated'}, status=401)

        try:
            account = Account.objects.get(app_secret_token=app_secret_token)

            # Check if there are linked destinations
            linked_destinations = Destination.objects.filter(account=account)
            if linked_destinations.exists():
                linked_destinations.delete()
                # If you want to prevent deletion of the account when linked destinations exist, 
                # return JsonResponse({'error': 'Linked destinations exist. Remove the links before deleting this account.'}, status=400)
            
            # Delete the account
            account.delete()
            return JsonResponse({'success': 'Account deleted successfully'})

        except Account.DoesNotExist:
            return JsonResponse({'error': 'Invalid App Secret Token'}, status=401)
        except Destination.DoesNotExist:
            pass

        return JsonResponse({'error': 'Unexpected error'}, status=500)