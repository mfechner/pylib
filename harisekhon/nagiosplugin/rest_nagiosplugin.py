#!/usr/bin/env python
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2016-12-19 17:42:51 +0000 (Mon, 19 Dec 2016)
#
#  https://github.com/harisekhon/pylib
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Rest API Check Specialization of NagiosPlugin

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import os
import sys
import traceback
# Python 2.6+ only
from abc import ABCMeta, abstractmethod
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import log, log_option
    from harisekhon.utils import validate_host, validate_port, validate_user, validate_password
    from harisekhon.nagiosplugin import NagiosPlugin
    from harisekhon import RequestHandler
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


class RestNagiosPlugin(NagiosPlugin):

    __version__ = __version__
    # abstract class
    __metaclass__ = ABCMeta

    def __init__(self):
        # Python 2.x
        super(RestNagiosPlugin, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = None
        self.default_host = 'localhost'
        self.default_port = 80
        self.default_user = None
        self.default_password = None
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.protocol = 'http'
        self.msg = 'rest msg not defined yet'
        self.request = RequestHandler()
        self.path = None
        self.ok()

    def add_options(self):
        self.add_hostoption(name=self.name,
                            default_host=self.default_host,
                            default_port=self.default_port)
        self.add_useroption(name=self.name,
                            default_user=self.default_user,
                            default_password=self.default_password)
        self.add_ssl_option()

    def add_ssl_option(self):
        self.add_opt('-S', '--use-ssl', action='store_true', default=False, help='Use SSL')

    def process_options(self):
        self.no_args()
        self.host = self.get_opt('host')
        self.port = self.get_opt('port')
        self.user = self.get_opt('user')
        self.password = self.get_opt('password')
        validate_host(self.host)
        validate_user(self.user)
        validate_password(self.password)
        validate_port(self.port)
        use_ssl = self.get_opt('use_ssl')
        log_option('ssl', use_ssl)
        if use_ssl and self.protocol == 'http':
            self.protocol = 'https'

    def run(self):
        req = self.query()
        self.parse(req)

    def query(self):
        url = '{proto}://{host}:{port}/'.format(proto=self.protocol,
                                                host=self.host,
                                                port=self.port)
        if self.path:
            url += self.path.lstrip('/')
        auth = None
        if self.user and self.password:
            log.info('authenicating to rest API')
            auth = (self.user, self.password)
        req = self.request.get(url, auth=auth)
        return req

    @abstractmethod
    def parse(self, req):
        pass