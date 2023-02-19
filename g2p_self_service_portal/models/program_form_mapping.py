from odoo import api, fields, models

class G2PProgram(models.Model):
    _inherit = "g2p.program"

    self_service_portal_form = fields.Many2one("website.page", string="Select Form")
