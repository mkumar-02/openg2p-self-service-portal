from odoo.addons.base_rest.controllers import main


class FormApiController(main.RestController):
    _root_path = "/api/v1/form/"
    _collection_name = "base.rest.form.services"
    _default_auth = "user"
