from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    self_service_logo = fields.Many2one(
        "ir.attachment",
        config_parameter="g2p_self_service_portal.self_service_logo_attachment",
    )

    self_service_signup_id_type = fields.Many2one(
        "g2p.id.type",
        config_parameter="g2p_self_service_portal.self_service_signup_id_type",
    )

    self_service_file_upload_size = fields.Char(
        "File Size",
        config_parameter="g2p_self_service_portal.self_service_file_upload_size",
    )
