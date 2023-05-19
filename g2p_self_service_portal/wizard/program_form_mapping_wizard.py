# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class G2PCreateProgramWizard(models.TransientModel):
    _inherit = "g2p.program.create.wizard"

    self_service_portal_form = fields.Many2one(
        "website.page",
        string="Program Form",
        domain="[('is_portal_form', '=', 'True')]",
    )

    def create_program(self):
        res = super(G2PCreateProgramWizard, self).create_program()

        program = self.env["g2p.program"].browse(res["res_id"])
        program_form_id = self.self_service_portal_form.id

        if program_form_id:
            program.update({"self_service_portal_form": program_form_id})

        return res
