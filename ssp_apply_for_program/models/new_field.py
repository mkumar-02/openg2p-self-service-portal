import json
from odoo import models,fields,api


class CustomJSONField(fields.Field):

    type = 'json'
    column_type = ('json', 'json')

    def __init__(self, string, **kwargs):
        self.column_type = ('json', 'json')

        super(CustomJSONField, self).__init__(string= string, **kwargs)

    def convert_to_cache(self, value, record, validate=True):
        if value and not isinstance(value, dict):
            return json.loads(value)
        return value

    def convert_to_record(self, value, record):
        if value:
            return json.dumps(value)
        return value


class G2PAdditionalData(models.Model):
    _inherit = "res.partner"

    additional_data = CustomJSONField(string="Additional Data")


