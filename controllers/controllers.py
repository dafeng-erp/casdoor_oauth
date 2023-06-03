# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.web.controllers import main as webMain
from odoo.http import request
from odoo.addons.web.controllers import main

class DfErpCasdoorSiteAuth(main.Home):
    """

    """

    def get_site_casdoor_setting(self, site_name):
        pass

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

    @http.route('/df_erp_casdoor_site_auth/login_call_back', auth='public')
    def login_callback(self, **kw):
        return "Hello, world"

    @http.route('/df_erp_casdoor_site_auth/login_call_back', auth='public')
    def user_info(self, **kw):
        return "Hello, world"

    def query_site_auth_setting(self,):
        pass

    def login_or_signup(self, email, password):
        """
        检测是否存在
        :param email:
        :param password:
        :return:
        """
        uid = request.session.authenticate(request.db, request.params['login'], request.params['password'])

        password

    @http.route('/df_erp_casdoor_site_auth/df_erp_casdoor_site_auth/objects', auth='public')
    def list(self, **kw):
        return http.request.render('df_erp_casdoor_site_auth.listing', {
            'root': '/df_erp_casdoor_site_auth/df_erp_casdoor_site_auth',
            'objects': http.request.env['df_erp_casdoor_site_auth.df_erp_casdoor_site_auth'].search([]),
        })

    @http.route(
        '/df_erp_casdoor_site_auth/df_erp_casdoor_site_auth/objects/<model("df_erp_casdoor_site_auth.df_erp_casdoor_site_auth"):obj>',
        auth='public')
    def object(self, obj, **kw):
        return http.request.render('df_erp_casdoor_site_auth.object', {
            'object': obj
        })
