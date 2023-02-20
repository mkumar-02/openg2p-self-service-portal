{
    "name": "G2P Self Service Portal",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://github.com/OpenG2P/openg2p-self-service-portal",
    "license": "Other OSI approved licence",
    "development_status": "Alpha",
    "depends": [
        "g2p_registry_base",
        "g2p_registry_individual",
        "g2p_programs",
        ],
    "data": [
        "views/g2p_self_service_base.xml",
        "views/g2p_self_service_login.xml",
        "views/g2p_self_service_dashboard.xml",
        "views/g2p_self_service_allprograms.xml",
        "views/g2p_self_service_myprofile.xml",
        "views/auth_oauth_provider.xml",
        "views/res_config_settings.xml",
        "views/g2p_self_service_program_view.xml"
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [],
        "web.assets_frontend": [
        
        ],
        "web.assets_common": [
            # "g2p_self_service_portal/static/src/css/base.css",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
