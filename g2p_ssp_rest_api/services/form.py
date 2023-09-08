from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component
from odoo.addons.g2p_registry_rest_api.models.individual_search_param import IndividualSearchParam

from ..models.spp_form import SSPFormInfoOut


class SPPFormApiService(Component):
    _inherit = ["base.rest.service"]
    _name = "spp.form.rest.service"
    _usage = "form"
    _collection = "base.rest.form.services"
    _description = """
        SPP Form API Services
    """

    @restapi.method(
        [
            (
                [
                    "/<int:id>",
                ],
                "GET",
            )
        ],
        output_param=PydanticModel(SSPFormInfoOut),
        auth="user",
        cors="*",
    )
    def get(self, _id):
        """
        Get program's information
        """
        program = self.env["g2p.program"].sudo().search([("id", "=", _id)])
        return SSPFormInfoOut.from_orm(program)

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=PydanticModel(IndividualSearchParam),
        output_param=PydanticModelList(SSPFormInfoOut),
        auth="user",
        cors="*",
    )
    def search(self, partner_search_param):

        programs = self.env["g2p.program"].sudo()
        active_programs = programs.search([("state", "=", "active")])

        res = []

        for program in active_programs:
            res.append(SSPFormInfoOut.from_orm(program))

        return res
