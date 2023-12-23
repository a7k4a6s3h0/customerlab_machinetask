from django.urls import path
from .views import * 

urlpatterns = [
    path('server/incoming_data', IncomingDataView.as_view(), name='server/incoming_data'),
    path('destinations/', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations/<str:account_id>/', DestinationByAccountView.as_view(), name='destination-by-account'),

    path('addDestination', Add_Destination.as_view(), name='addDestination'),
    path('UpdateDestination', UpdateDestination.as_view(), name='UpdateDestination'),
    path('DeleteDestination', deleteDestination.as_view(), name='DeleteDestination')

]
