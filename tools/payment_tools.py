'''
A collection of methods and classes to faciliate payment
'''

from constants.APIS import MOMO
from decouple import config
import requests

def make_momo_payment(transaction_code, amount):
    '''
    Make payment through momo. Normally, you would have to call me
    from an end point that generates the transaction_code.
    

    @input transaction_code: string that uniquely identifies a transaction
            the code must exist already in the database.
    
    @input amount: the amount to pay
    
    @output HTTP status of the result of the payment attempt
    '''

    headers = {
        'Authorization': '',
        'X-Callback-Url': '',
        'X-Reference-Id': transaction_code,
        'X-Target-Environment': '',
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config('MOMO_API_KEY'),
    }

    payment_data = {
        "amount": amount,
        "currency": "ugs",
        "externalId": transaction_code,
        "payer": {
          "partyIdType": "MSISDN",
          "partyId": "string"
        },
        "payerMessage": "string",
        "payeeNote": "string"
      }

    # alter the URL used as necessary based on payment mode selected
    # payment_option_detail array holds media (phone for e.g) and operator (e.g. mtn)

    # for now it is just mtn mobile money
    try:
        response = requests.post(
            MOMO['new_collection_request'], headers=headers, json=payment_data)
        payment_result = response.status_code
    except:
        payment_result = 500

    return payment_result