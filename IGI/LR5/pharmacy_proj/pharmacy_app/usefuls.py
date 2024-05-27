def is_in_groups(*groups):
    def is_in_groups_inner(user):
        return any(user.groups.filter(name=group).exists() for group in groups)
    
    return is_in_groups_inner