# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

import random
from datetime import datetime

from odoo import api, fields, models


class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    application_id = fields.Char(
        "Application ID", compute="_compute_application_id", store=True
    )

    @api.depends("partner_id")
    def _compute_application_id(self):
        for rec in self:
            d = datetime.today().strftime("%d")
            m = datetime.today().strftime("%m")
            y = datetime.today().strftime("%y")

            random_number = str(random.randint(1, 100000))

            rec.application_id = d + m + y + random_number.zfill(5)
