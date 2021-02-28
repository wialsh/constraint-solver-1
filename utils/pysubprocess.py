# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:00:29 2019

@author: wialsh

E-mail: hebiyaozizhou@gmail.com
"""
import os, sys, shlex
import subprocess


class StdError(RuntimeError):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        self.args = (status, message)

    @staticmethod
    def get_errors(error_string):
        return u' '.join(
            line for line in error_string.decode('utf-8').splitlines()
        ).strip()


class InputError(EnvironmentError):
    def __init__(self,cmd):
        super().__init__(
            "check your cmd: " + ','.join(cmd)
        )

def subprocess_args(include_stdout=True, **kwargs):
    # See https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
    # for reference and comments.
    def assign_value(key, value=None):
        kwargs[key] = kwargs.get(key, value)

    # kwargs = {
    #     'stdin': subprocess.PIPE,
    #     'stderr': subprocess.PIPE,
    #     'startupinfo': None,
    #     'env': None
    # }

    # https://stackoverflow.com/questions/24670668/subprocess-call-to-remove-files/24670879
    assign_value('stdin', subprocess.PIPE)
    assign_value('stderr', subprocess.PIPE)
    assign_value('startupinfo')
    assign_value('env')

    if hasattr(subprocess, 'STARTUPINFO'):
        kwargs['startupinfo'] = subprocess.STARTUPINFO()
        kwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs['env'] = os.environ

    if include_stdout:
        kwargs['stdout'] = subprocess.PIPE

    # kwargs['stderr'] = subprocess.STDOUT

    return kwargs

def run(cmd, **kwargs):
    if isinstance(cmd, str):
        cmd_args = cmd
        kwargs['shell'] = True
    else:
        cmd_args = []
        cmd_args += cmd
    print(' '.join(cmd_args) if isinstance(cmd_args, list) else cmd_args)

    relocation_stderr = kwargs.get('stderr', subprocess.PIPE) == subprocess.STDOUT
    try:
        proc = subprocess.Popen(cmd_args, **subprocess_args(**kwargs))
    except OSError:
        raise InputError(cmd_args)
    if relocation_stderr:
        content = ''
        while proc.poll() is None:
            line = proc.stdout.readline().decode('utf8').strip()
            if line != '':
                print(line)
                content += line + '\n'
        status_code = proc.returncode
    else:
        status_code, error_string = proc.wait(), proc.stderr.read()
        proc.stderr.close()

        if status_code:
            # raise StdError(status_code, StdError.get_errors(error_string))
            content = error_string.strip()
            try:
                print(content.decode('utf8').strip())
            except:
                print(content.decode('GB2312').strip())
        else:
            content = proc.stdout.read().strip()
    return status_code, content
