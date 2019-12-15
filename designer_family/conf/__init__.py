# Copyright 2015 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import

from oslo_log import log as logging
from oslo_middleware import cors
from oslo_policy import opts as policy_opts

from designer_family.conf import api
from designer_family.conf import base
from designer_family.conf import database
from designer_family.conf import paths
from designer_family.conf import placement


# To avoid global config, we require an existing ConfigOpts to be passed
# to register_opts. Then the caller can have some assurance that the
# config they are using will maintain some independence.
def register_opts(conf):
    api.register_opts(conf)
    base.register_opts(conf)
    database.register_opts(conf)
    paths.register_opts(conf)
    placement.register_opts(conf)
    logging.register_options(conf)
    policy_opts.set_defaults(conf)
    # The CORS middleware does not present a register_opts method, instead
    # it shares a list of available opts.
    conf.register_opts(cors.CORS_OPTS, 'cors')
