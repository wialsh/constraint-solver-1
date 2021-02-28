# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:49:52 2019

@author: wialsh

E-mail: hebiyaozizhou@gmail.com
"""
from typing import Dict, List, Any
import json, time
import urllib, urllib.request, urllib.parse
from urllib import error

import traceback

from . import Logger

HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}
TIMEOUT = 60

class Requesters(object):

    _name = 'request_test'
    _localfile = 'myrequest_test'


    def responses(self, url, data=None, headers=None, timeout=None, sleep=0.0, bad_request_sleep=30):
        #type: (str, Any, Dict, float, float, float) -> str
        content = None
        headers = headers or HEADERS
        timeout = timeout or TIMEOUT
        for i in range(10):
            try:
                response = urllib.request.Request(url,data=data,headers=headers)
                response = urllib.request.urlopen(response,timeout=timeout)
                content  = response.read()
                time.sleep(sleep)
                break
            except error.URLError as e:
                status = 'error' if i == 9 else 'warning'
                self.log.write('times: %s' % i, status=status, is_print=True)
                self.log.write('url: ' + url, status=status, is_print=True)
                if data is not None:
                    self.log.write('data: {}'.format(data), status=status, is_print=True)
                self.log.write(traceback.format_exc(), status=status, is_print=True)

                if hasattr(e, 'code') and e.code == 404:
                    break
                elif hasattr(e, 'reason') and e.reason == 'Not Found':
                    break
                time.sleep(bad_request_sleep)
        return content

    def decode(self, url, content=None, data=None):
        if content is None:
            msg = '''content is none, url='{}'; \n\t\t data='{}';'''.format(url, json.dumps(data))
            self.log_write(msg, status='warning', is_print=True)
            return None

        try:
            result = json.loads(content)
            try:
                status = int(result.get('status', 200))
            except:
                status = 0

            if status != 200 and (status > 10 or status < 0):
                msg = '''result['status'] != 200, url='{}'; \n\t\t data='{}';'''.format(url, json.dumps(data))
                self.log_write(msg, status='warning', is_print=True)

                self.log_write(json.dumps(result), is_print=True)

                return None
        except:
            result = content.decode('utf8') if isinstance(content, bytes) else content

        return result

    def request(self, url, *args, **kwargs):
        """
        This should be overridden in a base(sub) class.
        """
        raise NotImplementedError

    def quote(self,string, quote_plus=False, safe='/'):
        if quote_plus:
            return urllib.parse.quote_plus(string, safe=safe)
        else:
            return urllib.parse.quote(string, safe=safe)

    def log_write(self, content, status='info', is_print=False):
        try:
            self.log.write(content, status=status, is_print=is_print)
        except:
            print(content)

    @property
    def log(self):
        try:
            return self.__log
        except:
            self.__log = type(
                self._name,
                (self.logger,),
                dict(_localfile=self._localfile,_name=self._name)
            )() #type: Logger
            return self.__log

    @property
    def args(self):
        return (self._localfile, self._name,)

    @property
    def logger(self):
        return Logger
