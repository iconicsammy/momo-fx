'''
A collection of background tasks
'''

#from celery.task.schedules import crontab
from __future__ import absolute_import, unicode_literals
from payment.models import MomoRequest
from constants.APIS import MOMO
from decouple import config
import asyncio
from aiohttp import ClientSession
from app.celery import app



async def send_check_status(url, session):
    '''
    Sends the actual check payment status request

    '''
    headers = {
        'Authorization': '',
        'X-Target-Environment': '',
        'Ocp-Apim-Subscription-Key': config('MOMO_API_KEY'),
    }
    async with session.get(url, headers = headers) as response:
        return await response.json()

async def process_payments(payments):
    '''
    Make async requests to the payments
    @input payments query object
    '''
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for payment in payments:
            url = MOMO['check_payment_status'] % (payment.transaction_code)
            task = asyncio.ensure_future(send_check_status(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        update_payment_status(responses, payments)

def update_payment_status(results, payments):
    '''
    After all the HTTP Calls are finished, update the status of the
    payments.
    @input results: an array of http responses
    @input payments: an array of payment ORM objects
    '''

    counter = 0
    for result in results:
        if result['statusCode'] == 200:
            # note the API returns 200 but still it might have failed
            if result['status'] == 'SUCCESSFUL':
                payments[counter].status = 'Pending'
                payments[counter].save()
        counter = counter + 1




@app.task(name="check_payment_status")
def check_payment_status():
    '''
    Check pending payments and get their latest status
    '''
    pending_payments = MomoRequest.objects.filter(status='Pending')

    if pending_payments:
        # we have payments. check their status now

        #define a new event loop
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(process_payments(pending_payments))
        loop.run_until_complete(future)
