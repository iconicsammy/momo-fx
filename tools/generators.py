
from datetime import date, datetime
import string
import random
import time

import uuid
import hashlib


def generateTransactionCode(user_id):
    '''
    Generate a payment transaction code

    @input user_id: the id of the user the transaction is attached with

    @output string: sha256

    '''
    time_now = time.time()
    tm = ''.join([str(time_now), str(user_id)])
    remain = 50 - len(tm)
    rands = ''.join(random.choice(string.digits) for _ in range(remain))
    code = ''.join([tm, rands])
    code = hashlib.sha256(code.encode()).hexdigest()
    return code