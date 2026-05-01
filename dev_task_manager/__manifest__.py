{
    'name': 'Developer Task Manager',
    'version': '1.0',
    'summary': 'A simple and meaningful task tracker for developers',
    'description': 'Manage developer tasks, assign users, and track progress.',
    'category': 'Project',
    'author': 'maaz.waheed',
    'depends': ['base'], # 'base' is required to access standard Odoo features like Users
    'data':[
        'security/ir.model.access.csv',
        'views/dev_task_views.xml',
    ],
    'installable': True,
    'application': True,
}