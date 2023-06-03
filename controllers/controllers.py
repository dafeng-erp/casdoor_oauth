# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Request
from odoo.addons.web.controllers import main as webMain
from odoo.addons.auth_signup.controllers import main as signUpMain
from .casdoor import CasdoorSDK
from ..models.models import df_erp_casdoor_site_auth
import logging
import werkzeug.utils
import uuid

logger = logging.getLogger(__name__)


class DfErpCasdoorSiteAuth(http.Controller):
    """

    """

    def get_site_casdoor_setting(self, request_session):
        logger.debug("df:casdoor:request:{0} {1}".format(request_session, ''))
        if request_session.website is None:
            return None
        website_id = request_session.website.id
        website_domain = request_session.website.domain
        setting_model = request_session.env['df.auth.setting']
        search_domain = [
            ("domain_id", "=", website_id),
        ]
        logger.debug("df:casdoor:query:{0}".format(search_domain))
        if_existed = setting_model.sudo().search_count(search_domain
                                                       )
        if if_existed:
            return setting_model.sudo().search(
                search_domain, limit=1
            ).read()[0]
        else:
            return None

    def get_site_casdoor_user(self, request_session, website_id, login, **kwargs):
        user_model = request_session.env['df.auth.user']
        search_domain = [
            ("domain_id", "=", website_id),
            ("user_email", "=", login),
        ]
        logger.debug("df:casdoor:query:{0}".format(search_domain))
        if_existed = user_model.sudo().search_count(search_domain)
        if not if_existed:
            new_user = {
                "domain_id": website_id,
                "user_email": login,
                "password": kwargs.get('password'),
                "odoo_uid": kwargs.get('odoo_uid'),
                "casdoor_extra": kwargs.get("casdoor_extra")
            }
            new_user.update(kwargs)
            user_model.sudo().create(new_user)
        return user_model.sudo().search(
            search_domain, limit=1
        ).read()[0]

    @http.route('/web/df-erp/login', type='http', auth="public", methods=['GET'], website=True)
    def df_erp_web_login(self, redirect=None, **kw):
        logger.debug("casdoor:login:{0}".format(redirect))
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        return werkzeug.utils.redirect(casdoor_setting_model.get('casdoor_login_url', '/web/login'), 302)

    @http.route('/web/admin/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        super(DfErpCasdoorSiteAuth, self).web_login(redirect=redirect, **kw)

    @http.route('/x/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        logger.debug("casdoor:login:{}", redirect)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        if casdoor_setting_model is None:
            super(DfErpCasdoorSiteAuth, self).web_login(redirect=redirect, **kw)
        else:
            return request.redirect(casdoor_setting_model['casdoor_login_url'], 303)

    @http.route('/web/df-erp/login_callback', auth='public', methods=['GET', 'POST'], website=True)
    def login_callback(self, **kw):
        uid = self.login_or_signup(request)
        request.params['login_success'] = True
        redirect = "/web/login_successful"
        return request.redirect(redirect)

    def query_site_auth_setting(self, ):
        self.env['df.auth.setting'].search

    def login_or_signup(self, request_session):
        """
        {'owner': 'dourawards', 'name': 'test-login', 'createdTime': '2023-06-02T22:55:36+08:00', 'updatedTime': '', 'id': 'fd194c4f-027f-495a-8acb-8ee6c042a689', 'type': 'normal-user', 'password': '', 'passwordSalt': '', 'displayName': 'test-login', 'firstName': '', 'lastName': '', 'avatar': 'https://cdn.casbin.org/img/casbin.svg', 'permanentAvatar': '', 'email': 'jffoeg@example.com', 'emailVerified': False, 'phone': '71600376754', 'location': '', 'address': [], 'affiliation': 'Example Inc.', 'title': '', 'idCardType': '', 'idCard': '', 'homepage': '', 'bio': '', 'region': '', 'language': '', 'gender': '', 'birthday': '', 'education': '', 'score': 0, 'karma': 0, 'ranking': 2, 'isDefaultAvatar': False, 'isOnline': False, 'isAdmin': True, 'isGlobalAdmin': True, 'isForbidden': False, 'isDeleted': False, 'signupApplication': 'dourawards.com', 'hash': '', 'preHash': '', 'createdIp': '', 'lastSigninTime': '', 'lastSigninIp': '', 'ldap': '', 'properties': {}, 'roles': [], 'permissions': [], 'lastSigninWrongTime': '', 'signinWrongTimes': 0, 'tokenType': 'access-token', 'tag': 'staff', 'scope': 'read', 'iss': 'https://auth.dafengstudio.cn', 'sub': 'fd194c4f-027f-495a-8acb-8ee6c042a689', 'aud': ['774cec2af07a88c8b554'], 'exp': 1691847464, 'nbf': 1685799464, 'iat': 1685799464, 'jti': 'admin/c0a69378-4f03-48f0-a1c6-ade8dc012e95'}

        检测是否存在
        :param email:
        :param password:
        :return:
        """
        casdoor_setting_model: df_erp_casdoor_site_auth = self.get_site_casdoor_setting(request_session)
        website_id = request_session.website.id
        website_domain = request_session.website.domain
        query_params = request_session.get_http_params()
        code = query_params['code']
        state = query_params['state']
        casdoor_sdk: CasdoorSDK = CasdoorSDK(
            casdoor_setting_model['casdoor_endpoint'],
            casdoor_setting_model['casdoor_client_id'],
            casdoor_setting_model['casdoor_client_secret'],
            casdoor_setting_model['casdoor_certificate'],
            casdoor_setting_model['casdoor_org_name'],
            casdoor_setting_model['casdoor_application_name']
        )
        token = casdoor_sdk.get_oauth_token(code=code)
        logger.debug("df:casdoor:sdk:code={0} state={1} token={2}".format(code, state, token))
        access_token = token.get("access_token")
        decoded_msg = casdoor_sdk.parse_jwt_token(access_token)
        logger.debug("decoded_msg:{0}".format(decoded_msg))
        email = decoded_msg.get('email')
        domain = [(
            "login", '=', email,
        ), ("website_id", '=', website_id)]
        import xmlrpc.client
        url = 'http://127.0.0.1:8069'
        models = xmlrpc.client.ServerProxy('{0}/xmlrpc/2/object'.format(url))
        # if_existed = request_session.env['res.users'].sudo().search_count(domain)
        if_existed = models.execute_kw(request_session.db,
                                       casdoor_setting_model['operation_user_id'],
                                       casdoor_setting_model['operation_password'], 'res.users', 'search_count',
                                       (domain,))
        default_password = "{0}".format(uuid.uuid4())
        password = casdoor_setting_model["default_password"] or default_password
        logger.debug("df:casdoor:create_new_user:password:{0}".format(password))
        if not if_existed:
            create_new_user = {
                "login": email,
                "new_password": password,
                "password": password,
                "active": True,
                "name": decoded_msg.get("displayName", email),
                "notification_type": "email",
                "website_id": website_id
            }
            logger.debug("df:casdoor:create_new_user:{0}".format(create_new_user))
            user_id = models.execute_kw(request_session.db,
                                        casdoor_setting_model['operation_user_id'],
                                        casdoor_setting_model['operation_password'], 'res.users', 'create',
                                        [
                                            create_new_user,
                                        ])
            logger.debug("df:casdoor:create_new_user:{0}".format(user_id))
            """
            user_ids = models.execute_kw(request_session.db,
                                     casdoor_setting_model['operation_user_id'],
                                     casdoor_setting_model['operation_password'], 'res.users', 'search',
                                     (domain, 0, 1))
            """
            user = self.get_site_casdoor_user(request_session, website_id, email, password=password)
        else:
            user = self.get_site_casdoor_user(request_session, website_id, email, password=password)
        """
        user = models.execute_kw(request_session.db,
                                 casdoor_setting_model['operation_user_id'],
                                 casdoor_setting_model['operation_password'], 'res.users', 'read',
                                 (user_ids, ['login', 'password'])
                                 )[0]
        """
        logger.debug("df:casdoor:auth:user:{0}".format(user))
        # request_session.env['res.users'].sudo(1).search(domain).read()[0]
        uid = request_session.session.authenticate(request_session.db, user['user_email'],
                                                   user['password'])
        """
        uid = request_session.session.authenticate(request_session.db, request_session.params['login'],
                                                   request_session.params['password'])
       
        """
        logger.debug("df:casdoor:auth:uid:{0}".format(uid))
        return uid


class DfErpCasdoorSiteRegister(http.Controller):
    """

    """

    def get_site_casdoor_setting(self, request):
        if request.website is None:
            return None
        website_id = request.website.id
        website_domain = request.website.domain
        setting_model = request.env['df.auth.setting']
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

    @http.route('/web/df-erp/signup', type='http', auth='public', website=True, sitemap=False, methods=['GET'], )
    def df_erp_web_auth_signup(self, *args, **kw):
        logger.debug("casdoor:signup:{}", args)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        return request.redirect(casdoor_setting_model.casdoor_register_url, 303)

    @http.route('/x/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        logger.debug("casdoor:signup:{}", args)
        casdoor_setting_model = self.get_site_casdoor_setting(request)
        if casdoor_setting_model is None:
            super(DfErpCasdoorSiteRegister, self).web_auth_signup(*args, **kw)
        else:
            return request.redirect(casdoor_setting_model['casdoor_register_url'], 303)
