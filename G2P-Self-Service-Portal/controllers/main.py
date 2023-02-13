from odoo import http
from odoo.http import Controller, request, route


class Dashboard(Controller):
    @route("/allprograms", website=True, auth="public")
    def AllPrograms(self, **kw):
        programs = request.env["g2p.program"].sudo().search([]).sorted('id')
        total = programs.search_count([])
        page=total/10
        programs = request.env["g2p.program"].sudo().search([],offset=(page - 1) * 10, limit=10).sorted('id')
        
        
        pager = request.website.pager(
            url='/allprograms',
            total=total,
            page=page,
            step=10,
        )
        partner_id = request.env.user.partner_id
        states = {'draft': 'Submitted', 'enrolled': 'Enrolled'}

        values = []
        for program in programs:
            membership = request.env["g2p.program_membership"].sudo().search(
                [('partner_id', '=', partner_id.id), ('program_id', '=', program.id)])
            values.append({
                'id': program.id,
                'name': program.name,
                'has_applied': len(membership) > 0,
                'status': states.get(membership.state, 'Error')

            })

        return request.render(
            "G2P-Self-Service-Portal.allprograms",
            {
                'programs': values
            }
        )

    @route("/", website=True, auth="public")
    def MyPrograms(self, **kw):

        programs = request.env["g2p.program"].sudo().search([]).sorted('id')
        partner_id = request.env.user.partner_id
        states = {'draft': 'Submitted', 'enrolled': 'Enrolled'}


        values = []
        for program in programs:
            membership = request.env["g2p.program_membership"].sudo().search(
                [('partner_id', '=', partner_id.id), ('program_id', '=', program.id)])
            ammount_issued = sum([ent.ammount for ent in request.env['g2p.entitlement'].sudo().search(
                [('partner_id', '=', request.session.uid), ('program_id', '=', program.id)])])
            values.append({
                'id': program.id,
                'name': program.name,
                'has_applied': len(membership) > 0,
                'status': states.get(membership.state, 'Error'),
                'issued': ammount_issued,
           
                'enrollment_date': membership.enrollment_date
            })

        return request.render(
            "G2P-Self-Service-Portal.main_page",
            {
                'programs': values
            },
        )
