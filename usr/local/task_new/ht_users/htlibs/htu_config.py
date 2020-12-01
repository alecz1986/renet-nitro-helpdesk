#
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append('/usr/local/fshop/pylibs')

secret_minlength = 7
base_dir = '/usr/local/task_new'
htroot_dir = os.path.join(base_dir, 'ht_users')
templates_dir = os.path.join(htroot_dir, 'templates')
sessions_dir = os.path.join(htroot_dir, 'sessions')
admin_dir = os.path.join(base_dir, 'ht_admin')
htdocs_dir = os.path.join(admin_dir, 'htdocs')
prod_dir = os.path.join(htdocs_dir, 'product')
dbi_info = 'mysql://admintask:rom724Kz@localhost/tasks_new?charset=utf8&use_unicode=1'
