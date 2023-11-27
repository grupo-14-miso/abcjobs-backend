

def remove_password_properties(entity):
    if 'password_hash' and 'salt' in entity:
        del entity['password_hash']
        del entity['salt']
    return entity
