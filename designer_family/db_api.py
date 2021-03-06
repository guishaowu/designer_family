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
"""Database context manager for designer_family database connection."""

from oslo_db.sqlalchemy import enginefacade
from oslo_log import log as logging

from designer_family.util import run_once

LOG = logging.getLogger(__name__)
placement_context_manager = enginefacade.transaction_context()


def _get_db_conf(conf_group):
    conf_dict = dict(conf_group.items())
    # Remove the 'sync_on_startup' conf setting, enginefacade does not use it.
    # Use pop since it might not be present in testing situations and we
    # don't want to care here.
    conf_dict.pop('sync_on_startup', None)
    return conf_dict


@run_once("TransactionFactory already started, not reconfiguring.",
          LOG.warning)
def configure(conf):
    placement_context_manager.configure(
        **_get_db_conf(conf.placement_database))


def get_placement_engine():
    return placement_context_manager.writer.get_engine()


@enginefacade.transaction_context_provider
class DbContext(object):
    """Stub class for db session handling outside of web requests."""
