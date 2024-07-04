from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('populate_data', views.populate_data, name='populate_data'),
    path('send_email_message', views.send_email_message, name='send_email_message'),
    path('get_bills', views.get_bills, name='get_bills'),
]



