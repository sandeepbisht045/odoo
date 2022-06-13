{
    'name': 'Hospital Management',
    'version': '12.0.1.0.0.0',
    'category': 'Extra Tools',
    'summary': 'Module for managing the hospitals',
    'sequence': '10',
    'license' : 'AGPL-3',
    'author': 'Odoo Mates',
    'maintainer': 'Odoo Mates',
    'website': 'odoomates.com',
    'depends': ['mail','sale',],
    'demo': [],
    'data': ["wizards/create_appointment.xml","views/patient.xml","data/sequence.xml","data/cron.xml",
             "views/appointment.xml","reports/report.xml",
             'reports/patient_card.xml',"data/data.xml","security/security.xml",
             "security/ir.model.access.csv","data/mail_template.xml","views/lab.xml"


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}