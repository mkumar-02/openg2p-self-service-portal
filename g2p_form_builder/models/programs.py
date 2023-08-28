# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class G2PProgram(models.Model):
    _inherit = "g2p.program"

    self_service_portal_form = fields.Many2one(
        "formio.builder",
        string="Program Form",
        domain="[('is_portal_form', '=', 'True')]",
    )
