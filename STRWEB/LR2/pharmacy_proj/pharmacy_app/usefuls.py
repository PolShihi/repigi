def is_in_groups(*groups):
    def is_in_groups_inner(user):
        f = False
        
        if ('Admin' in groups):
            if user.is_superuser:
                f = True
                
        l = [user.groups.filter(name=group).exists() for group in groups]
        l.append(f)
        return any(l)
    
    return is_in_groups_inner