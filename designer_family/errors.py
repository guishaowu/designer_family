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
"""Error code symbols to be used in structured JSON error responses.

These are strings to be used in the 'code' attribute, as described by
the API guideline on `errors`_.

There must be only one instance of any string value and it should have
only one associated constant SYMBOL.

In a WSGI handler (representing the sole handler for an HTTP method and
URI) each error condition should get a separate error code. Reusing an
error code in a different handler is not just acceptable, but useful.

For example 'designer_family.inventory.inuse' is meaningful and correct in both
``PUT /resource_providers/{uuid}/inventories`` and ``DELETE`` on the same
URI.

.. _errors: http://specs.openstack.org/openstack/api-wg/guidelines/errors.html
"""

# NOTE(cdent): This is the simplest thing that can possibly work, for now.
# If it turns out we want to automate this, or put different resources in
# different files, or otherwise change things, that's fine. The only thing
# that needs to be maintained as the same are the strings that API end
# users use. How they are created is completely fungible.


# Do not change the string values. Once set, they are set.
# Do not reuse string values. There should be only one symbol for any
# value.
# Don't forget to document new error codes in api-ref/source/errors.inc.
DEFAULT = 'designer_family.undefined_code'
INVENTORY_INUSE = 'designer_family.inventory.inuse'
CONCURRENT_UPDATE = 'designer_family.concurrent_update'
DUPLICATE_NAME = 'designer_family.duplicate_name'
PROVIDER_IN_USE = 'designer_family.resource_provider.inuse'
PROVIDER_CANNOT_DELETE_PARENT = (
    'designer_family.resource_provider.cannot_delete_parent')
RESOURCE_PROVIDER_NOT_FOUND = 'designer_family.resource_provider.not_found'
ILLEGAL_DUPLICATE_QUERYPARAM = 'designer_family.query.duplicate_key'
# Failure of a post-schema value check
QUERYPARAM_BAD_VALUE = 'designer_family.query.bad_value'
QUERYPARAM_MISSING_VALUE = 'designer_family.query.missing_value'
