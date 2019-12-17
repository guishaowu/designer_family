#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright 2013 IBM Corp.
# Copyright 2013 eNovance <licensing@enovance.com>
# Copyright Ericsson AB 2013. All rights reserved
# Copyright 2014 Hewlett-Packard Company
# Copyright 2015 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from designer_family.api.controllers.v2 import capabilities
from pecan import expose, redirect, request
from webob.exc import status_map
import logging
import uuid
import shutil
LOG = logging.getLogger(__name__)


class RootController(object):
    @expose(generic=True, template='index.html')
    def index(self):
        return dict()

    @index.when(method='POST')
    def index_post(self, q):
        print(q)
        redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)

    @expose(generic=True, template="upload_file.html")
    def pre_upload(self):
        return dict()

    @expose()
    def upload(self):
        LOG.error("test")
        LOG.error(request.POST['file'])
        LOG.error(request.POST['file'].file)
        data = request.POST['file'].file
        path = "/root/static/"
        file_path = path + str(uuid.uuid4())
        with open(file_path, 'bw') as file_obj:
            shutil.copyfileobj(data, file_obj)

