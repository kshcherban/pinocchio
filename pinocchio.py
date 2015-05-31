#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license: GPL v2
# author: Konstantin Shcherban <k.scherban@gmail.com>

from __future__ import print_function
import os
import sys
import yaml
import time
import argparse
from subprocess import Popen, PIPE
from multiprocessing import Pool


def logger(*message):
    logtime = time.strftime('%b %d %H:%M:%S')
    try:
        print(logtime, *message, file=logfile)
    except:
        pass


def yaml_parser(yaml_file):
    try:
        yaml_dict = yaml.load(yaml_file)
    except Exception, err:
        logger('ERROR: Can not parse', yaml_file, err)
        sys.exit(1)
    return yaml_dict


def git_clone(module_dict):
    module = module_dict['name']
    git = module_dict['git']
    ref = module_dict['ref']
    mod_path = module_dict['dir'] + '/' + module
    if os.path.isdir(mod_path):
        message = 'INFO: Pulling {0} into {1} from {2}/{3}'
        message = message.format(module, mod_path, git, ref)
        cmd = '''cd {0} && /usr/bin/git pull &&
        /usr/bin/git remote set-url origin {1} &&
        /usr/bin/git checkout {2} && /usr/bin/git merge origin/{2}'''
        cmd = cmd.format(mod_path, git, ref)
    else:
        message = 'INFO: Cloning {0} into {1} from {2}/{3}'
        message = message.format(module, mod_path, git, ref)
        cmd = '/usr/bin/git clone --depth 1 --no-single-branch -b {0} {1} {2}'
        cmd = cmd.format(ref, git, mod_path)
    child = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    if child.wait():
        message = '{0} {1} {2}'.format(
            'ERROR processing',
            module,
            child.communicate()[1].strip())
    return message

parser = argparse.ArgumentParser(prog='pinocchio')
parser.add_argument('-l', '--logfile',
                    type=argparse.FileType('a'),
                    default=sys.stderr,
                    help='Log file destination, default: stderr')
parser.add_argument('-p', '--parallel',
                    type=int,
                    default=24,
                    help='Parallel processes, default: 24')
parser.add_argument('puppetfile',
                    type=argparse.FileType('r'),
                    help='Path to puppetfile.yaml, mandatory')
if __name__ == '__main__':
    args = parser.parse_args()
    logfile = args.logfile
    modules_dir = os.path.dirname(os.path.abspath(args.puppetfile.name))
    modules_dict = yaml_parser(args.puppetfile)
    modules_arr = []
    for m in modules_dict:
        module_dict = modules_dict[m]
        module_dict['dir'] = modules_dir
        module_dict['name'] = m
        if not 'ref' in modules_dict[m]:
            modules_dict[m]['ref'] = 'master'
        modules_arr.append(module_dict)
    pool = Pool(processes=args.parallel)
    output = pool.map(git_clone, modules_arr, 1)
    pool.close()
    pool.join()
    for log in output:
        logger(log)
