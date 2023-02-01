{
    'name': 'G2P Self Service Portal',
    'version': '15.0.0.0.1',
    'description': '''
     portal which helps user to utilize services
    ''',
    'summary': 'G2P Self Service Portal',
    'author': 'OpenG2P',
    'website': '#',
    'license': 'LGPL-3',
    'category': 'G2P',
    'depends': [
        'base','website'
    ],
    'data': [
	  'views/main-dashboard.xml',
      'views/all-programs.xml'

    ],

    "application": False,
    "installable": True,
    "auto_install": False,
    'assets': {
        
    }
}
