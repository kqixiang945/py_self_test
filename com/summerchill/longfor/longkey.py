# -*- coding: utf-8 -*-
import hashlib
import hmac
import time
from jproperties import Properties

configs = Properties()
with open('/Users/kongxiaohan/.lauth', 'rb') as config_file:
    configs.load(config_file)
    key = configs.get("key").data

_START_TIME = 1167609600
_TIME_STEP = 60
now = time.time()
intervals_no = (int(now) - _START_TIME) // _TIME_STEP
h = hmac.new(bytes(key, encoding='utf-8'), bytes(str(intervals_no), encoding='utf-8'), hashlib.sha1)
lating_str = h.digest()
lating_length = len(lating_str)
o = lating_str[len(lating_str) - 1] & 15
truncation_offset = 31
if (truncation_offset >= 0 and truncation_offset < (lating_length - 4)):
    o = truncation_offset
binary = ((lating_str[o] & 127) << 24) \
         | ((lating_str[o + 1] & 255) << 16) \
         | ((lating_str[o + 2] & 255) << 8) \
         | (lating_str[o + 3] & 255)
otp = str(binary % 1000000)
while (len(otp) < 6):
    otp = '0' + otp
totp = str(otp).zfill(6)
print(totp)
