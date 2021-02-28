"""
Created on Thu May 21 19:20:52 2020

@author: wialsh

@e-mail: hebiyaozizhou@gmail.com
"""

import logging, os, re
import datetime

class Logger(object):
    _date = f'{datetime.datetime.now().date()}'

    _re_date = re.compile(r'(\d{4}-\d{2}-\d{2})')
    _re_suffix = re.compile('\.(txt|dat|log|out)')
    info_name = 'debug.log'
    error_name = 'error.log'
    _name = 'test'

    save_path = ''
    info_file = ''
    error_file = ''

    _f_handler = None

    def __init__(self, info_name=None, name=None,):
        if info_name:
            self.__class__.info_name = info_name
        if name:
            self.__class__._name = name

        self.__get_log_file_path()

        #https://www.cnblogs.com/yyds/p/6901864.html
        info_file = self.__class__.info_file
        name = self.__class__._name
        LOG_FORMAT = "【%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s(:%(lineno)d)】\n%(message)s"

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)


        rf_handler = logging.FileHandler(info_file)
        rf_handler.setLevel(logging.INFO)
        rf_handler.setFormatter(logging.Formatter(LOG_FORMAT))


        logger.addHandler(rf_handler)
        self._logger = logger
        self.handlers_duplicates()
        # print(self._logger.handlers)


    def add_handler_error(self):
        if any(map(lambda x: self.__class__.error_file in x.baseinfo_name, self._logger.handlers)):
            error_file = self.__class__.error_file
            LOG_FORMAT_ERROR = "【%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s(:%(lineno)d)]】\n%(message)s"
            f_handler = logging.FileHandler(error_file)
            f_handler.setLevel(logging.ERROR)
            # f_handler.set_name('ERROR')
            f_handler.setFormatter(logging.Formatter(LOG_FORMAT_ERROR))
            self._logger.addHandler(f_handler)
            self.handlers_duplicates()

    @classmethod
    def from_external(cls, info_name, name):
        return cls(info_name, name)

    @classmethod
    def from_name(cls, name='test'):
        return cls(info_name=cls.info_name, name=name)

    def write(self, content, status='info', is_print=False, *args, **kwargs):

        if status == 'info':
            self._logger.info(content, *args, **kwargs)
        elif status == 'warning':
            self._logger.warning(content, *args, **kwargs)
        elif status == 'error':
            self.add_handler_error()
            self._logger.error(content, *args, **kwargs)
        else:
            self._logger.info(content, *args, **kwargs)

        if is_print: print(content)


    def close(self):
        del self._logger

    @property
    def logging_file(self):
        return self.__class__.info_file

    def handlers_duplicates(self):
        handlers_size = len(self._logger.handlers)
        handlers_new = []
        level_list = []

        handlers = self._logger.handlers
        handlers.reverse()
        for i in range(handlers_size):
            handler = handlers[i]
            level = handler.level
            if level in level_list:
                pass
            else:
                handlers_new.append(handler)
                level_list.append(level)

        self._logger.handlers.clear()
        # self._logger.handlers = handlers_new
        for handler in handlers_new:
            self._logger.addHandler(handler)
                
    
    def __get_log_file_path(self):
        save_path = self.__class__.save_path

        info_file = self.__class__._re_suffix.sub('', self.__class__.info_name)
        error_file = self.__class__._re_suffix.sub('', self.__class__.error_name)
        # print(save_path)
        if self._re_date.findall(info_file) == []:
            info_file_new = os.path.join(save_path, f'{info_file}{self.__class__._date}.log')
            error_file = os.path.join(save_path, f'{error_file}{self.__class__._date}.log')
        else:
            info_file_new = os.path.join(save_path, f'{info_file}.log')
            error_file = os.path.join(save_path, f'{error_file}.log')

        self.__class__.info_file = info_file_new.replace('\\', '/')
        self.__class__.error_file = error_file.replace('\\', '/')


    @property
    def info(self):
        return self._logger.info

    @property
    def warning(self):
        return self._logger.warning

    @property
    def error(self):
        return self._logger.error

    @property
    def critical(self):
        return self._logger.critical

    def __repr__(self):
        return f'''{str(__class__)[:-1]}, logger name: '{self.__class__._name}', file handler: '{self.info_file}' >'''
