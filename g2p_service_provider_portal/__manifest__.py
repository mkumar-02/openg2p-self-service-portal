{
    "name": "G2P Service Provider Portal",
    "category": "G2P",
    "version": "15.0.1.1.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "Other OSI approved licence",
    "development_status": "Alpha",
    "depends": [
        "g2p_self_service_portal",
        "g2p_program_reimbursement",
    ],
    "data": [
        "views/base.xml",
        "views/dashboard.xml",
        "views/reimbursement.xml",
        "views/form_page_template.xml",
        "views/form_submitted.xml",
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [],
        "web.assets_frontend": [
            "g2p_service_provider_portal/static/src/js/form_action.js",
        ],
        "web.assets_common": [],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
