# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_erp_casdoor_site_auth(models.Model):
    """
    https://github.com/casdoor/casdoor-python-sdk
    """
    _name = 'df_erp_casdoor_site_auth.df_erp_casdoor_site_auth'
    _description = 'cassdor登录配置'

    casdoor_login_url = fields.Char()
    casdoor_register_url = fields.Char()
    domain_name = fields.Char()
    casdoor_endpoint = fields.Char()
    casdoor_client_id = fields.Char()
    casdoor_client_secret = fields.Char()
    casdoor_certificate = fields.Binary()
    casdoor_org_name = fields.Char()
    default_password = fields.Char()
    description = fields.Text()
    last_update_time = fields.Datetime()


class df_erp_casdoor_site_auth_user(models.Model):
    """
    https://github.com/casdoor/casdoor-python-sdk
    """
    _name = 'df_erp_casdoor_site_auth.extra_user'
    _description = 'cassdor登录配置'

    user_email = fields.Char()
    user_name = fields.Char()
    domain_name = fields.Char()
    password = fields.Char()
    user_id = fields.Char()
    casdoor_code = fields.Char()
    casdoor_extra = fields.Json()
    description = fields.Text()
    info = fields.Json()
    last_update_time = fields.Datetime()
