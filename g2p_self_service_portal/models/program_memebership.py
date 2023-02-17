from odoo import api, fields, models

class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    application_id = fields.Float("Application ID")

