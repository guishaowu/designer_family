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


from oslo_db.sqlalchemy import models
from oslo_log import log as logging
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Unicode

LOG = logging.getLogger(__name__)


class _Base(models.ModelBase, models.TimestampMixin):
    pass


BASE = declarative_base(cls=_Base)


class ResourceClass(BASE):
    """Represents the type of resource for an inventory or allocation."""
    __tablename__ = 'resource_classes'
    __table_args__ = (
        schema.UniqueConstraint("name", name="uniq_resource_classes0name"),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)


class ResourceProvider(BASE):
    """Represents a mapping to a providers of resources."""

    __tablename__ = "resource_providers"
    __table_args__ = (
        Index('resource_providers_uuid_idx', 'uuid'),
        schema.UniqueConstraint('uuid', name='uniq_resource_providers0uuid'),
        Index('resource_providers_name_idx', 'name'),
        Index('resource_providers_root_provider_id_idx',
              'root_provider_id'),
        Index('resource_providers_parent_provider_id_idx',
              'parent_provider_id'),
        schema.UniqueConstraint('name', name='uniq_resource_providers0name')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(String(36), nullable=False)
    name = Column(Unicode(200), nullable=True)
    generation = Column(Integer, default=0)
    # Represents the root of the "tree" that the provider belongs to
    root_provider_id = Column(
        Integer, ForeignKey('resource_providers.id'), nullable=True)
    # The immediate parent provider of this provider, or NULL if there is no
    # parent. If parent_provider_id == NULL then root_provider_id == id
    parent_provider_id = Column(
        Integer, ForeignKey('resource_providers.id'), nullable=True)


class Inventory(BASE):
    """Represents a quantity of available resource."""

    __tablename__ = "inventories"
    __table_args__ = (
        Index('inventories_resource_provider_id_idx',
              'resource_provider_id'),
        Index('inventories_resource_class_id_idx',
              'resource_class_id'),
        Index('inventories_resource_provider_resource_class_idx',
              'resource_provider_id', 'resource_class_id'),
        schema.UniqueConstraint(
            'resource_provider_id', 'resource_class_id',
            name='uniq_inventories0resource_provider_resource_class')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    resource_provider_id = Column(Integer, nullable=False)
    resource_class_id = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    reserved = Column(Integer, nullable=False)
    min_unit = Column(Integer, nullable=False)
    max_unit = Column(Integer, nullable=False)
    step_size = Column(Integer, nullable=False)
    allocation_ratio = Column(Float, nullable=False)
    resource_provider = orm.relationship(
        "ResourceProvider",
        primaryjoin=('Inventory.resource_provider_id == '
                     'ResourceProvider.id'),
        foreign_keys=resource_provider_id)


class Allocation(BASE):
    """A use of inventory."""

    __tablename__ = "allocations"
    __table_args__ = (
        Index('allocations_resource_provider_class_used_idx',
              'resource_provider_id', 'resource_class_id',
              'used'),
        Index('allocations_resource_class_id_idx',
              'resource_class_id'),
        Index('allocations_consumer_id_idx', 'consumer_id')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    resource_provider_id = Column(Integer, nullable=False)
    consumer_id = Column(String(36), nullable=False)
    resource_class_id = Column(Integer, nullable=False)
    used = Column(Integer, nullable=False)
    resource_provider = orm.relationship(
        "ResourceProvider",
        primaryjoin=('Allocation.resource_provider_id == '
                     'ResourceProvider.id'),
        foreign_keys=resource_provider_id)


class ResourceProviderAggregate(BASE):
    """Associate a resource provider with an aggregate."""

    __tablename__ = 'resource_provider_aggregates'
    __table_args__ = (
        Index('resource_provider_aggregates_aggregate_id_idx',
              'aggregate_id'),
    )

    resource_provider_id = Column(Integer, primary_key=True, nullable=False)
    aggregate_id = Column(Integer, primary_key=True, nullable=False)


class PlacementAggregate(BASE):
    """A grouping of resource providers."""
    __tablename__ = 'placement_aggregates'
    __table_args__ = (
        schema.UniqueConstraint("uuid", name="uniq_placement_aggregates0uuid"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), index=True)


class Trait(BASE):
    """Represents a trait."""

    __tablename__ = "traits"
    __table_args__ = (
        schema.UniqueConstraint('name', name='uniq_traits0name'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(Unicode(255), nullable=False)


class ResourceProviderTrait(BASE):
    """Represents the relationship between traits and resource provider"""

    __tablename__ = "resource_provider_traits"
    __table_args__ = (
        Index('resource_provider_traits_resource_provider_trait_idx',
              'resource_provider_id', 'trait_id'),
    )

    trait_id = Column(Integer, ForeignKey('traits.id'), primary_key=True,
                      nullable=False)
    resource_provider_id = Column(Integer,
                                  ForeignKey('resource_providers.id'),
                                  primary_key=True,
                                  nullable=False)


class Project(BASE):
    """The project is the Keystone project."""

    __tablename__ = 'projects'
    __table_args__ = (
        schema.UniqueConstraint(
            'external_id',
            name='uniq_projects0external_id',
        ),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    external_id = Column(String(255), nullable=False)


class User(BASE):
    """The user is the Keystone user."""

    __tablename__ = 'users'
    __table_args__ = (
        schema.UniqueConstraint(
            'external_id',
            name='uniq_users0external_id',
        ),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    external_id = Column(String(255), nullable=False)


class Consumer(BASE):
    """Represents a resource consumer."""

    __tablename__ = 'consumers'
    __table_args__ = (
        Index('consumers_project_id_uuid_idx', 'project_id', 'uuid'),
        Index('consumers_project_id_user_id_uuid_idx', 'project_id', 'user_id',
              'uuid'),
        schema.UniqueConstraint('uuid', name='uniq_consumers0uuid'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column(String(36), nullable=False)
    project_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    generation = Column(Integer, nullable=False, server_default="0", default=0)


class Designer(BASE):
    """Represents a designer."""

    __tablename__ = 'designers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(100), nullable=False)
    skills = Column(Text, nullable=True)
    work_experiences = Column(Text, nullable=True)
    education_experiences = Column(Text, nullable=True)
    awards = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    contract = Column(Boolean, default=False)
    authentication = Column(Boolean, default=False)
    address = Column(String(100), nullable=True)
    salary = Column(Integer, nullable=True)
    project_rate = Column(Integer, nullable=True)
    tags = Column(String(200))
    projects = orm.relationship(
        "ConstructionProject", backref='Designer')


class ConstructionProject(BASE):
    """Represents a constrction project."""

    __tablename__ = 'construction_projects'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(100), nullable=False)
    area = Column(Float)
    city = Column(String(20), nullable=True)
    tags = Column(String(200), nullable=True)
    team = Column(String(100), nullable=True)
    design_time = Column(DateTime, nullable=True)
    designer_id = Column(Integer, ForeignKey('designers.id'))


class Person(BASE):
    __tablename__ = 'person'
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
