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

from oslo_config import cfg

api_group = cfg.OptGroup(
    'api',
    title='API options',
    help="""
Options under this group are used to define Placement API.
""")

api_opts = [
    cfg.StrOpt(
        "auth_strategy",
        default="noauth2",
        choices=("keystone", "noauth2"),
        deprecated_group="DEFAULT",
        help=""),
    cfg.StrOpt(
        "paste_config",
        default="api-paste.ini",
        help=""),
]


def register_opts(conf):
    conf.register_group(api_group)
    conf.register_opts(api_opts, group=api_group)


def list_opts():
    return {api_group: api_opts}
