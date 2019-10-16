class FilterModule(object):
    def acl_state(self,acl_def):
        for acl_name, acl_rules in acl_def.items():
            for rule in acl_rules:
                rule['state'] = rule['state'].upper()
        return acl_def
    
    def custom_acl(self,acl_def,field=None):
        for acl_name, acl_rules in acl_def.items():
            for rule in acl_rules:
                if field and field in rule.keys():
                    rule[field] = rule[field].upper()
        return acl_def

    def filters(self):
        return {
            'acl_state': self.acl_state,
            'custom_acl': self.custom_acl
        }

