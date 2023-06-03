# -*- coding: utf-8 -*-

from odoo import models, fields, api


class df_erp_casdoor_site_auth(models.Model):
    """
    https://github.com/casdoor/casdoor-python-sdk
    """
    _name = 'df.auth.setting'
    _description = 'cassdor登录配置'

    casdoor_login_url = fields.Char()
    casdoor_register_url = fields.Char()
    casdoor_forget_url = fields.Char()
    domain_name = fields.Char()
    domain_id = fields.Char()
    casdoor_endpoint = fields.Char()
    casdoor_client_id = fields.Char()
    casdoor_client_secret = fields.Char()
    casdoor_certificate = fields.Text()
    casdoor_org_name = fields.Char()
    casdoor_application_name = fields.Char()
    default_password = fields.Char()
    operation_user = fields.Char()
    operation_user_id = fields.Char()
    operation_password = fields.Char()
    description = fields.Text()
    last_update_time = fields.Datetime()


class df_erp_casdoor_site_auth_user(models.Model):
    """
    https://github.com/casdoor/casdoor-python-sdk
    """
    _name = 'df.auth.user'
    _description = 'cassdor登录配置'

    user_email = fields.Char()
    user_name = fields.Char()
    domain_name = fields.Char()
    domain_id = fields.Char()
    odoo_uid = fields.Char()
    password = fields.Char()
    user_id = fields.Char()
    casdoor_code = fields.Char()
    casdoor_extra = fields.Json()
    description = fields.Text()
    info = fields.Json()
    last_update_time = fields.Datetime()
