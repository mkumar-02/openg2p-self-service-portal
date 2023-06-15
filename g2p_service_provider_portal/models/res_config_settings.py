from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    service_provider_file_upload_size = fields.Float(
        "File Size",
        config_parameter="g2p_service_provider_portal.service_provider_file_upload_size",
    )
