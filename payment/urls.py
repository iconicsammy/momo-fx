from django.conf.urls import url

from payment import views
urlpatterns = [
    url(r'^view-payment-requests/$', views.viewMoMoRequests.as_view(), name='view-payment-requests'),
    url(r'^new-request/$', views.createNewMoMoRequest.as_view(), name='new-request'),

    ]
