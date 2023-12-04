#!/usr/bin/env python
# coding=utf-8

import hashlib
import hmac
import base64
import requests
import time
import json

import findIp

# Signature Make
def make_signature(method, basestring, timestamp, access_key, secret_key):
    
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    
    secret_key = bytes(secret_key, 'utf-8')  # secret_key를 바이트로 변환
    message = bytes(message, 'utf-8')  # message를 바이트로 변환
    
    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
    return signature


def requestApi(timestamp, access_key, signature, uri):
    
    # Header for Request
    headers = {'x-ncp-apigw-timestamp': timestamp,
               'x-ncp-iam-access-key': access_key,
               'x-ncp-apigw-signature-v2': signature}

    # Geolocation API Request
    res = requests.get(uri, headers=headers)

    # Check Response
    # print('status : %d' % res.status_code)
    # print('content : %s' % res.content)
    
    json_data = json.loads(res.content)
    
    # json에서 "lat"와 "long" value parsing 
    latitude = json_data['geoLocation']['lat']
    longitude = json_data['geoLocation']['long']

    return latitude,longitude


def findMyLocation():
    # Signature 생성에 필요한 항목
    myip = findIp.get_public_ip()
    method = "GET"
    basestring = "/geolocation/v2/geoLocation?ip={}&ext=t&responseFormatType=json".format(myip)
    timestamp = str(int(time.time() * 1000))
    access_key = "{your_access_key}"  # access key id (from portal or sub account)
    secret_key = "{your_secret_key}"  # secret key (from portal or sub account)
    signature = make_signature(method, basestring, timestamp, access_key, secret_key)
    
    # GET Request
    hostname = "https://geolocation.apigw.ntruss.com"
    requestUri = hostname + basestring
    lat, long = requestApi(timestamp, access_key, signature, requestUri)
    return lat, long