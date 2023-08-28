import pydantic

from odoo.addons.g2p_programs_rest_api.models import program
from odoo.addons.g2p_registry_rest_api.models.naive_orm_model import NaiveOrmModel


class SelfServicePortalForm(NaiveOrmModel):
    name: str = None
    form_json_schema: str = pydantic.Field(..., alias="schema")


class SelfServicePortalFormInfoOut(
    program.ProgramInfoOut, extends=program.ProgramInfoOut
):
    self_service_portal_form: SelfServicePortalForm = None
