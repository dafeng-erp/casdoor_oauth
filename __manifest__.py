# -*- coding: utf-8 -*-
{
    'name': "df_erp_casdoor_site_auth",

    'summary': """
       用于对接casdoor的登录, 多站点情况下独立走casdoor
       """,

    'description': """
       用于对接casdoor的登录, 多站点情况下独立走casdoor
    """,

    'author': "dafeng-erp",
    'website': "https://www.dafengstudio.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'website', 'auth_signup', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/dferp_casdoor_site_auth_login.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        # 'web.assets_backend': [
        #    'jrizju_extra_module/static/src/js/component.js'
        # ],
        'web.assets_frontend': [
            "casdoor_oauth/static/src/js/casdoor-js-sdk.js",
            "casdoor_oauth/static/src/js/casdoor-login.js",
        ]},
    'installable': True,
    "application": True,
}
