import json
import datetime
import random
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
        return request.render("ssp_apply_for_program.custom_main",{'value': value_to_pass})

    @http.route("/apply_for_program", type="http", website=True, auth="public")
    def program_controller(self, **kw):
        value_to_pass = "4Ps"
        return request.render("ssp_apply_for_program.example_body",{'value': value_to_pass})


    @http.route("/website/form", type="http", website=True, auth="public")
    def apply_to_program(self, **kw):

        # Adding Additional data to the res.partner model
        form_data = {}
        
        current_user = request.env.user
        form_data['address'] = json.dumps(kw)
        form_data['additional_info'] = json.dumps(kw)

        request.env['res.partner'].sudo().search([("name", "=", current_user.name)]).write(form_data)

        # Enrolling user to Program
        program_name = "4Ps"
        program_id = request.env['g2p.program'].sudo().search([('name', '=', program_name),]).id
    

        #Passing submission date and application date to the view
        today_date = datetime.date.today().strftime("%d-%b-%Y")

        d = datetime.date.today().strftime("%d")
        m = datetime.date.today().strftime("%m")
        y = datetime.date.today().strftime("%y")

        random_number= str(random.randint(1,100000))

        def random_number_length(n):
            n = str(n)
            l = len(n)
            if (l<5):
                while l>5:
                    n = '0'+ n
                    l = l+1
                return '0'+n
        
            return n

        application_id = int(d+ m+ y+ random_number_length(random_number))

        apply_to_program = {
            'partner_id': current_user.partner_id.id,
            'program_id': program_id,
            'application_id': application_id
        }

        print(apply_to_program)

        request.env['g2p.program_membership'].sudo().create(apply_to_program)

        return request.render("ssp_apply_for_program.form_submitted",{"submission_date": today_date, "application_id": application_id})



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



