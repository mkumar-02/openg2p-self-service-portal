# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

from odoo import models


class G2PClaimProgram(models.Model):
    _inherit = "g2p.program"

    def update_form_template(self):
        if self.is_claims_program:
            form_view = self.self_service_portal_form.view_id
            form_view_template = form_view.arch_db
            form_view.write(
                {
                    "arch_db": form_view_template.replace(
                        "website.layout",
                        "g2p_claims_portal.claim_submission_form_template",
                    ).replace(
                        "g2p_self_service_portal.self_service_form_template",
                        "g2p_claims_portal.claim_submission_form_template",
                    )
                }
            )
        else:
            return super(G2PClaimProgram, self).update_form_template()
