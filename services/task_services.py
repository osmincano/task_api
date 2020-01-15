# -*- coding: utf-8 -*-
# Copyright 2020
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component


class ProjectService(Component):
    _inherit = "base.rest.service"
    _name = "task.service"
    _usage = "task"
    _collection = "task.private.services"
    _description = """
        Task Services
        Access to the task services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get task's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name):
        """
        Searh task by name
        """
        tasks = self.env["project.task"].search([('name', 'ilike', name)])
        rows = []
        res = {"count": len(tasks), "rows": rows}
        for task in tasks:
            rows.append(self._to_json(task))
        return res

    # pylint:disable=method-required-super
    #def create(self, **params):
        #"""
        #Create a new task
        #"""
        #project = self.env["project.project"].create(self._prepare_params(params))
        #return self._to_json(project)

    #def update(self, _id, **params):
        #"""
        #Update project informations
        #"""
        #project = self._get(_id)
        #project.write(self._prepare_params(params))
        #return self._to_json(project)


    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["project.task"].browse(_id)

    def _prepare_params(self, params):
        return params

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    def _validator_create(self):
        res = {
            "name": {"type": "string", "required": True, "empty": False},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, project):
        res = {
            "id": project.id,
            "name": project.name,
        }
        return res
