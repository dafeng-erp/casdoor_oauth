# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.web.controllers import main as webMain
from odoo.http import request
from odoo.addons.web.controllers import main as webMain
from odoo.addons.auth_signup.controllers import main as signUpMain
from .casdoor import CasdoorSDK
from ..models.models import df_erp_casdoor_site_auth
import logging

logger = logging.getLogger(__name__)


class DfErpCasdoorSiteAuth(webMain.Home):
    """

    """

    def get_site_casdoor_setting(self, request):
        if request.website is None:
            return None
        website_id = request.website.id
        website_domain = request.website.domain
        setting_model = self.env['df.auth.setting']
        search_domain = [
            ("domain_id", "=", website_id),
        ]
        if_existed = setting_model.sudo().search_count(search_domain
                                                       )
        if if_existed:
            return setting_model.sudo().search(
                search_domain, limit=1
            ).read()[0]
        else:
            return None

    @http.route('/web/df-erp/login', type='http', auth="public", methods=['GET'])
    def web_login(self, redirect=None, **kw):
        logger.debug("casdoor:login:{}", redirect)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        return request.redirect(casdoor_setting_model.casdoor_login_url, 303)

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        logger.debug("casdoor:login:{}", redirect)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        if casdoor_setting_model is None:
            super(DfErpCasdoorSiteAuth, self).web_login(redirect=redirect, **kw)
        else:
            return request.redirect(casdoor_setting_model.casdoor_login_url, 303)

    @http.route('/web/df-erp/login_call_back', auth='public', methods=['GET', 'POST'])
    def login_callback(self, **kw):
        self.login_or_signup(request)
        return request.redirect('/web/login_successful', 303)

    def query_site_auth_setting(self, ):
        self.env['df.auth.setting'].search

    def login_or_signup(self, request):
        """
        检测是否存在
        :param email:
        :param password:
        :return:
        """
        casdoor_setting_model: df_erp_casdoor_site_auth = self.get_site_casdoor_setting(request)
        website_id = request.website.id
        website_domain = request.website.domain
        query_params = request.get_http_params()
        code = query_params['code']
        state = query_params['state']
        casdoor_sdk: CasdoorSDK = CasdoorSDK(
            casdoor_setting_model.casdoor_endpoint,
            casdoor_setting_model.casdoor_client_id,
            casdoor_setting_model.casdoor_client_secret,
            casdoor_setting_model.casdoor_certificate,
            casdoor_setting_model.casdoor_org_name,
        )
        token = casdoor_sdk.get_oauth_token(code=code)
        access_token = token.get("access_token")
        decoded_msg = casdoor_sdk.parse_jwt_token(access_token)
        logger.debug("decoded_msg:{}", decoded_msg)
        domain = [(
            "login", '=', "email"
        )]
        self.env['res.users'].search(domain)
        uid = request.session.authenticate(request.db, request.params['login'], request.params['password'])
        logger.debug("uid:{}", uid)

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


class DfErpCasdoorSiteRegister(signUpMain.AuthSignupHome):
    """

    """

    def get_site_casdoor_setting(self, request):
        if request.website is None:
            return None
        website_id = request.website.id
        website_domain = request.website.domain
        setting_model = self.env['df.auth.setting']
        search_domain = [
            ("domain_id", "=", website_id),
        ]
        if_existed = setting_model.sudo().search_count(search_domain
                                                       )
        if if_existed:
            return setting_model.sudo().search(
                search_domain, limit=1
            ).read()[0]
        else:
            return None

    @http.route('/web/df-erp/signup', type='http', auth='public', website=True, sitemap=False, methods=['GET'])
    def web_auth_signup(self, *args, **kw):
        logger.debug("casdoor:signup:{}", args)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        return request.redirect(casdoor_setting_model.casdoor_register_url, 303)

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        logger.debug("casdoor:signup:{}", args)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        if casdoor_setting_model is None:
            super(DfErpCasdoorSiteRegister, self).web_auth_signup(*args, **kw)
        else:
            return request.redirect(casdoor_setting_model.casdoor_register_url, 303)
