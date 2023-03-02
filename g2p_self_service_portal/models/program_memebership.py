import random
from datetime import datetime
from odoo import api, fields, models

class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    application_id = fields.Char("Application ID")

    @api.model
    def create(self, vals):

        if not vals.get('application_id', ''):
                 
            d = datetime.today().strftime("%d")
            m = datetime.today().strftime("%m")
            y = datetime.today().strftime("%y")

            random_number = str(random.randint(1, 100000))

            vals['application_id'] = d + m + y + random_number.zfill(5)

        return super(G2PProgramMembership, self).create(vals)

    

