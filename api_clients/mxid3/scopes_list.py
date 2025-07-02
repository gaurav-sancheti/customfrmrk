class Scopes:
    mx_company_read = "mx:company:read"
    mx_company_write = "mx:company:write"
    mx_company_brand_write = "mx:company:brand:write"
    mx_company_contact_validate = "mx:company:contact:validate"

    mx_mxid3_company_read = "mx:mxid3:company:read"
    mx_mxid3_company_create = "mx:mxid3:company:create"
    mx_mxid3_company_update = "mx:mxid3:company:update"
    mx_mxid3_company_delete = "mx:mxid3:company:delete"

    mx_mxid3_emaildomain_read = "mx:mxid3:emaildomain:read"
    mx_mxid3_emaildomain_create = "mx:mxid3:emaildomain:create"
    mx_mxid3_emaildomain_delete = "mx:mxid3:emaildomain:delete"

    @classmethod
    def generate_inherited_scopes(cls, scopes):
        new_scopes_list = []
        for scope in scopes:
            new_scopes_list.append(scope)
        return sorted(new_scopes_list)
