# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from os.path import join
from ConfigParser import ConfigParser

try:
    from deploy_env import DeployEnv
except ImportError:
    DeployEnv = 'dev'

try:
    from override import ConfigOverride
except ImportError:
    ConfigOverride = []

config = ConfigParser()
config.readfp(open(join(__path__[0], '_default.cfg')))
config.read([join(__path__[0], '%s.cfg' % DeployEnv)])
config.set('django', 'env', DeployEnv)

for (section, option, value) in ConfigOverride:
    config.set(section, option, value)

