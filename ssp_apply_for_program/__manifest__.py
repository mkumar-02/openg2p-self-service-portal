{
    "name": "G2P Self Service Portal: Apply For Program",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://github.com/OpenG2P/openg2p-self-service-portal",
    "license": "Other OSI approved licence",
    "development_status": "Production/Stable",
    "maintainers": ["jeremi", "gonzalesedwin1123"],
    "depends": ["website","web"],
    "data": [
        "data/action_data.xml",
        "views/header_template.xml",
        "views/form_page_layout.xml",
        "views/footer_template.xml",
        "views/detail.xml",
        "views/landing_view.xml",
        "views/submitted_view.xml",
        "views/ref.xml",
        "views/sample_form.xml",
        "views/website_page.xml",
        "views/form_submitted.xml"
        # "views/form_submit_button.xml"
    ],
    "css": [
        'static/src/css/tyles.css',
    ],
    "assets": {
        'web.assets_common':[
            ('prepend', 'ssp_apply_for_program/static/src/css/style.css'),
        ],
        'web.assets_backend': [
            'ssp_apply_for_program/static/src/css/style.css',
            'ssp_apply_for_program/static/src/js/form_action.js'
        ],
        'web.assets_frontend': [
            'ssp_apply_for_program/static/src/css/style.css',
            'ssp_apply_for_program/static/src/js/form_action.js'
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}