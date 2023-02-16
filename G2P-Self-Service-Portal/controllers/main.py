from datetime import datetime
from odoo import http
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
import math

class Dashboard(Controller):
    @route(['/allprograms'], website=True, auth="public")
    def AllPrograms(self, page="1", limit="5", search="", **kw):
        limit=int(limit)
        page=int(page)
        if page<1:
            page=1
        if limit<5:
            limit=5
        programs = request.env["g2p.program"].sudo().search(
            [], limit=limit, offset=(page - 1) * limit, order='id')

        total = math.ceil(request.env["g2p.program"].sudo().search_count([])/limit)
        # page_info = pager('/allprograms',total=total,page=page,step=5)

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
                'status': states.get(membership.state, 'Error'),

            })

        return request.render(
            "G2P-Self-Service-Portal.allprograms",
            {
                'programs': values,
                'pager': {
                    'sel': page,
                    'total': total,
                }

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
            # date = datetime.strptime(membership['enrollment_date'], '%Y-%m-%d')
            # output_date = date.strftime('%d-%b-%Y')
            ammount_issued = sum([ent.amount_issued for ent in request.env['g2p.payment'].sudo().search(
                [('partner_id', '=', request.session.uid), ('program_id', '=', program.id)])])
            values.append({
                'id': program.id,
                'name': program.name,
                'has_applied': len(membership) > 0,
                'status': states.get(membership.state, 'Error'),
                'issued': ammount_issued,
                'enrollment_date': membership.enrollment_date.strftime('%d-%b-%Y') if membership.enrollment_date else None

            })

        return request.render(
            "G2P-Self-Service-Portal.main_page",
            {
                'programs': values,
                'ammount_issued': ammount_issued,

            },
        )
