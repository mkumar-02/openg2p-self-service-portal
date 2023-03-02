from odoo import api, fields, models


class G2PProgram(models.Model):
    _inherit = "g2p.program"

    self_service_portal_form = fields.Many2one("website.page")

    @api.constrains("self_service_portal_form")
    def update_form_template(self):
        form_view = self.self_service_portal_form.view_id
        form_view_template = form_view.arch_db
        form_view.write(
            {
                "arch_db": form_view_template.replace(
                    "website.layout",
                    "g2p_self_service_portal.self_service_form_template",
                )
            }
        )


class G2PCreateProgramWizard(models.TransientModel):
    _inherit = "g2p.program.create.wizard"

    self_service_portal_form = fields.Many2one("website.page", "Program Form")
