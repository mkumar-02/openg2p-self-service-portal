from odoo import http
from odoo.http import Controller, request, route


class Dashboard(Controller):
    @route("/allPrograms", website=True, auth="public")
    def AllPrograms(self, **kw):
        programs = request.env["g2p.program"].sudo().search([])
        partner_id = request.env["res.users"].browse(request.session.uid).partner_id
        memberships = request.env["g2p.program_membership"].sudo().search([])
        
        return request.render(
            "G2P-Self-Service-Portal.all_programs",
            {
                "programs": programs,
                "partner_id":partner_id,
                "memberships": memberships
            },
        )

    @route("/", website=True, auth="public")
    def MyPrograms(self, **kw):
        programs = request.env["g2p.program"].sudo().search([])
        partner_id = request.env["res.users"].browse(request.session.uid).partner_id
        return request.render(
            "G2P-Self-Service-Portal.main_page",
            {
                "programs": programs,

            },
        )
