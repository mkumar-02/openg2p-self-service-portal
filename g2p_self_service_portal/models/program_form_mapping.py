from odoo import api, fields, models

class G2PProgram(models.Model):
    _inherit = "g2p.program"

    self_service_portal_form = fields.Selection([("form1", "Form 1")], "Program Form")
