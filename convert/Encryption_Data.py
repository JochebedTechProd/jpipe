#!/usr/bin/env python

import base64

from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])] # python2
#unpad = lambda s : s[0:-(s[-1])] # python3



class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        try: 
           raw = pad(raw)
           iv = Random.new().read( AES.block_size )
           cipher = AES.new( self.key, AES.MODE_CBC, iv )
           res = base64.b64encode( iv + cipher.encrypt( raw ) )
           return res
        except Exception as e :
           return {"Error":"True"}

    def decrypt( self, enc ):
        try:
           enc = base64.b64decode(enc)
           iv = enc[:16]
           cipher = AES.new(self.key, AES.MODE_CBC, iv )
           res = unpad(cipher.decrypt( enc[16:] ))
           #return unpad(cipher.decrypt( enc[16:] ))
           return res
        except Exception as e:
           return {"Error":"True"}

dev_key='BAJ_HCL_JTS_key1'
#adap_key='0000000000000001'
#key='jts/jpipe/v_0_0_1/data/dregister'
cipher = AESCipher(dev_key)
#cipher = AESCipher(adap_key)
encrypted = cipher.encrypt('This is a test. Count=1')
print("encrypted ="+encrypted+"=")
decrypted = cipher.decrypt(encrypted)
print("decrypted : ",decrypted)
#decrypted = cipher.decrypt("245JjPBUzmutrg0vAfbK+aPNkaeFHVwlfE5f4airjnSK+yxSElCQDIMT10KUsdwrAa4zZieurYTrwKO/0FwEHAOLSm/kNiG+Z4LcvFFVBrCtZs/K5QnfZV14LcoZjq/FuzHwcSQexFGjVeTbllMA6PVZFE/Vhc1DfhhSEoGD4ogAXoHCxnnqTVlxeN/8It7ebQ5Z3uewZvV42zjZhifqPg==")
#print ("decrypted : ",decrypted)
