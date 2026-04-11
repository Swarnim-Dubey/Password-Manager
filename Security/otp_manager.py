import time
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def get_expiry_time(minutes = 5):
    return int(time.time()) + (minutes * 60)

def is_otp_valid(stored_otp, stored_expiry, entered_otp):
    current_time = int(time.time())

    if current_time > stored_expiry:
        return False, "OTP Expired Now"
    
    if stored_otp != entered_otp:
        return False, "Wrong OTP Found"
    
    return True, "OTP Verified"