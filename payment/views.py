from common_imports import *
from payment.models import MomoRequest
from payment.serializer import MomoRequestSerializer
from django.db.models import F
from tools.generators import generateTransactionCode
from tools.payment_tools import make_momo_payment
# Create your views here.


class viewMoMoRequests(APIView):
    '''
    View current momo requests that have been sent to users
    
    Filters: pass filters by query string. Currently:
        - status : by status of the payment request (pending)
        - user : reqeusts made to a specific user
    '''

    permission_classes = []

    def get(self, request, format = None):
        response = {}

        filters = {}
        
        filter_by_status = request.query_params.get('status', '')
        filter_by_user = request.query_params.get('user', '')

        if filter_by_status:
            filters['status'] = filter_by_status
        
        if filter_by_user:
            filters['user_id'] = filter_by_user

        response['data'] = list(MomoRequest.objects.filter(**filters).annotate(
            first_name=F('user__first_name')).values('first_name','status','created_on','transaction_code', 'id'))

        return JsonResponse(response,status = 200)



class createNewMoMoRequest(APIView):
    '''
    Create a new momo request. Once it is saved,
    make an external API request
    '''
    permission_classes = []

    def post(self, request, format=None):
        # Get the data. purify it
        status = 400 # assume error
        data = request.data
        serializer = MomoRequestSerializer(data=data)
        response = {'message' : ''}
        if serializer.is_valid():
            content = serializer.validated_data
            transaction_code = generateTransactionCode(content['user_requested_for'])
            data =  {
                'user_id': content['user_requested_for'],
                'amount' : content['amount'],
                'transaction_code' : transaction_code
            }
            momo_request = MomoRequest(**data)
            
            momo_request.save()
            # is it successfully saved?
            if momo_request:
                # make API request now
                payment_result = make_momo_payment(transaction_code , content['amount'])
                if payment_result <= 202:
                    # success
                    status = 200
                    response['message'] = 'Payment sent. Confirm on your phone'
                else:
                    # the payment failed. delete the record we have saved
                    momo_request.delete()
                    response['message'] = 'There was an error connecting wit MoMo payment gateway'
            else:
                response['message'] = 'Error when saving your payment. Try again'
        
        else:
            # the data submitted has an error
            response['message'] = serializer.errors
            

        return JsonResponse(response, status = status)



