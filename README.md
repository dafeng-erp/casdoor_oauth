# casdoor_oauth

casdoor oauth for odoo16

## 原理

基于odoo多站点的模式下的授权机制, 登录使用 casdoor 类似中台
解耦出来

#### 登出按钮

```xhtml
<div id="o_logout_divider" class="dropdown-divider"/>
                    <a t-attf-href="/web/session/logout?redirect=/" role="menuitem" id="o_logout" class="dropdown-item ps-3">
                        <i class="fa fa-fw fa-sign-out me-1 small text-muted"/> Logout
</a>
        </div>
```

#### 登录按钮


```xhtml
<data name="User Sign In" inherit_id="portal.placeholder_user_sign_in">
        <xpath expr="." position="inside">
            <li t-nocache="Profile session and user group can change unrelated to parent caches." t-nocache-_item_class="_item_class" t-nocache-_link_class="_link_class" groups="base.group_public" t-attf-class="#{_item_class} o_no_autohide_item">
                <a t-attf-href="/web/login" t-attf-class="#{_link_class}">Sign in<span t-if="request.session.profile_session" class="text-danger fa fa-circle"/></a>
            </li>
        </xpath>
    </data>
```


## 使用






## 主题新增视图




http://git.dafengstudio.cn/dafeng_erp/casdoor_oauth