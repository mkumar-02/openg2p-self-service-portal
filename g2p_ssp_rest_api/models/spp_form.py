import pydantic

from odoo.addons.g2p_registry_rest_api.models.naive_orm_model import NaiveOrmModel


class SelfServicePortalForm(NaiveOrmModel):
    name: str = None
    form_json_schema: str = pydantic.Field(..., alias="schema")


class SSPFormInfoOut(NaiveOrmModel):
    id: int = None
    self_service_portal_form: SelfServicePortalForm = None
