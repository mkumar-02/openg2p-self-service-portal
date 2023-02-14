import json
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import form


class Website(http.Controller):

    @http.route("/4psform", type="http", website=True, auth="public")
    def all_program(self, **kw):
        return request.render("ssp_apply_for_program.sample_form",{})

    @http.route("/form_layout", type="http", website=True, auth="public")
    def all_program(self, **kw):
        value_to_pass = "4Ps"
        views = request.env['ir.ui.view'].browse(14912)
        print("------------------- current view ------------------")
        print(views.name)
        return request.render("ssp_apply_for_program.custom_main",{'value': value_to_pass, 'view': views})

    @http.route("/apply_for_program", type="http", website=True, auth="public")
    def program_controller(self, **kw):
        value_to_pass = "4Ps"
        return request.render("ssp_apply_for_program.example_body",{'value': value_to_pass})

    @http.route("/submit", type="http", website=True, auth="public")
    def apply_to_program(self, **kw):
        print("--------submit----------------------------")
        print(kw)
        return request.redirect("/")



class WebsiteForm(form.WebsiteForm):
    
    def _handle_website_form(self, model_name, **kwargs):
        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)

    def insert_record(self, request, model, values, custom, meta=None):
        model_name = model.sudo().model


        print(custom)
        custom_fields = custom.splitlines()
        print(custom_fields)

        custom_fields_data = {}
        for i in range(len(custom_fields)):
            custom_fields_data[custom_fields[i].split(':')[0].strip()]= custom_fields[i].split(':')[1].strip()
        
        print(custom_fields_data)

        values['name'] = 'manoj'
        values['is_registrant'] = True
        values['address'] = json.dumps(custom_fields_data)

        record = request.env[model_name].create(values)

        
        return record.id



# class WebsiteForm(form.WebsiteForm):
    
#     def _handle_website_form(self, model_name, **kwargs):
#         return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)

#     def insert_record(self, request, model, values, custom, meta=None):
#         model_name = model.sudo().model


#         print(custom)
#         custom_fields = custom.splitlines()
#         print(custom_fields)

#         custom_fields_data = {}
#         for i in range(len(custom_fields)):
#             custom_fields_data[custom_fields[i].split(':')[0].strip()]= custom_fields[i].split(':')[1].strip()
        
#         print("-------form aciton-----")
#         print(values)
#         values['name'] = values['family_name']+', '+ values['given_name']
#         values['is_registrant'] = True
#         record = request.env[model_name].create(values)

#         # Getting the user information
#         print(request.env.user)

#         # Enrolling user to the program
#         program_name = "4Ps"

#         program_id = request.env['g2p.program'].search([('name', '=', program_name),]).id
#         partner_id = record.id
        
#         apply_to_program = {
#             'partner_id': partner_id,
#             'program_id': program_id
#         }

#         request.env['g2p.program_membership'].create(apply_to_program)
        
#         return record.id



