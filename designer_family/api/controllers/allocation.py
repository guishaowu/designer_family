from designer_family.objects import usage as allo_obj
from pecan import expose, redirect, request
from designer_family import db_api


class AllocationController(object):

    @expose(template='json')
    def index(self):
        ctxt = db_api.DbContext()
        usage_list = allo_obj.get_all_by_project_user(ctxt, 'test')
        return {'usages': usage_list}
