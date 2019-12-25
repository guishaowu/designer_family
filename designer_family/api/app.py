#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright 2015-2016 Red Hat, Inc.
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

import os
import uuid
import logging as py_logging
import os
import os.path

from paste import deploy
import pecan
from oslo_config import cfg
from oslo_log import log as logging
from oslo_log import log
from oslo_middleware import cors
from oslo_utils import importutils
import pbr.version

from designer_family import conf as df_conf
from designer_family import db_api
from designer_family.api import hooks
from designer_family.api import middleware

osprofiler = importutils.try_import('osprofiler')
osprofiler_initializer = importutils.try_import('osprofiler.initializer')
profiler = importutils.try_import('osprofiler.opts')

CONFIG_FILE = 'designer_family.conf'

# The distribution name is required here, not package.
version_info = pbr.version.VersionInfo('openstack-designer_family')

LOG = log.getLogger(__name__)


# NOTE(sileht): pastedeploy uses ConfigParser to handle
# global_conf, since python 3 ConfigParser doesn't
# allow storing object as config value, only strings are
# permit, so to be able to pass an object created before paste load
# the app, we store them into a global var. But the each loaded app
# store it's configuration in unique key to be concurrency safe.
global APPCONFIGS
APPCONFIGS = {}


def setup_app(root, conf):
    app_hooks = [hooks.ConfigHook(conf),
                 hooks.TranslationHook()]
    template_path = os.path.dirname(__file__) + "/templates"
    return pecan.make_app(
        root,
        hooks=app_hooks,
        wrap_app=middleware.ParsableErrorMiddleware,
        guess_content_type_from_ext=False,
        template_path=template_path
    )


def load_app(conf):
    global APPCONFIGS

    # Build the WSGI app
    cfg_path = conf.api.paste_config
    if not os.path.isabs(cfg_path):
        cfg_path = conf.find_file(cfg_path)

    if cfg_path is None or not os.path.exists(cfg_path):
        raise cfg.ConfigFilesNotFoundError([conf.api.paste_config])

    config = dict(conf=conf)
    configkey = str(uuid.uuid4())
    APPCONFIGS[configkey] = config

    LOG.info("WSGI config used: %s", cfg_path)
    return deploy.loadapp("config:" + cfg_path,
                          name="designer_family+" + (
                              conf.api.auth_strategy
                              if conf.api.auth_strategy else "noauth"
                          ),
                          global_conf={'configkey': configkey})


def app_factory(global_config, **local_conf):
    global APPCONFIGS
    appconfig = APPCONFIGS.get(global_config.get('configkey'))
    return setup_app(root=local_conf.get('root'), **appconfig)


def setup_logging(config):
    # Any dependent libraries that have unhelp debug levels should be
    # pinned to a higher default.
    extra_log_level_defaults = [
        'routes=INFO',
    ]
    logging.set_defaults(default_log_levels=logging.get_default_log_levels() +
                         extra_log_level_defaults)
    logging.setup(config, 'designer_family')
    py_logging.captureWarnings(True)


def _get_config_files(env=None):
    """Return a list of one file or None describing config location.

    If None, that means oslo.config will look in the default locations
    for a config file.
    """
    if env is None:
        env = os.environ

    dirname = env.get('OS_DESIGNER_FAMILY_CONFIG_DIR', '').strip()
    if dirname:
        return [os.path.join(dirname, CONFIG_FILE)]
    else:
        return None


def _parse_args(config, argv, default_config_files):
    # register designer_family's config options
    df_conf.register_opts(config)

    if profiler:
        profiler.set_defaults(config)

    _set_middleware_defaults()

    config(argv[1:], project='designer_family',
           version=version_info.version_string(),
           default_config_files=default_config_files)


def setup_profiler(config):
    if osprofiler and config.profiler.enabled:
        osprofiler.initializer.init_from_conf(
            conf=config,
            context={},
            project="designer_family",
            service="designer_family",
            host="??")


def _set_middleware_defaults():
    """Update default configuration options for oslo.middleware."""
    cors.set_defaults(
        allow_headers=['X-Auth-Token',
                       'X-Openstack-Request-Id',
                       'X-Identity-Status',
                       'X-Roles',
                       'X-Service-Catalog',
                       'X-User-Id',
                       'X-Tenant-Id',
                       'OpenStack-API-Version'],
        expose_headers=['X-Auth-Token',
                        'X-Openstack-Request-Id',
                        'X-Subject-Token',
                        'X-Service-Token',
                        'OpenStack-API-Version'],
        allow_methods=['GET',
                       'PUT',
                       'POST',
                       'DELETE',
                       'PATCH']
    )


def build_wsgi_app(argv=None):
    conffiles = _get_config_files()

    config = cfg.ConfigOpts()
    df_conf.register_opts(config)

    # This will raise cfg.RequiredOptError when a required option is not set
    # (notably the database connection string). We want this to be a hard fail
    # that prevents the application from starting. The error will show up in
    # the wsgi server's logs.
    _parse_args(config, [], default_config_files=conffiles)
    # initialize the logging system
    setup_logging(config)

    # configure database
    db_api.configure(config)

    # dump conf at debug if log_options
    if config.log_options:
        config.log_opt_values(
            logging.getLogger(__name__),
            logging.DEBUG)

    return load_app(config)

application = build_wsgi_app()
