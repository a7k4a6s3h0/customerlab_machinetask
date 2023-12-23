from django.urls import path
from .views import *

urlpatterns = [

    path('CreateAccount',RegisterAccount.as_view(), name='CreateAccount'),
    path('UpdateAccount',UpdateAccount.as_view(), name='update_account'),
    path('DeleteAcccount', DeleteAccount.as_view(), name='DeleteAcccount'),
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),

]
