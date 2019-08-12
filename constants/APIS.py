'''
External APIS in use
'''
from decouple import config

MOMO = {
    'new_collection_request': 'https://ericssonbasicapi2.azure-api.net/collection/v1_0/requesttopay',
    'check_payment_status' : 'https://ericssonbasicapi2.azure-api.net/collection/v1_0/requesttopay/%s',
}