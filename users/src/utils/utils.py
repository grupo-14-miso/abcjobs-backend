from google.cloud import datastore


def get_entity_by_field(entity, field_name, field_value):
    # Initialize the Datastore client
    client = datastore.Client()

    # Query all Users
    query = client.query(kind=entity).add_filter(field_name, '=', field_value)
    results = list(query.fetch())
    try:
        return results.pop()
    except:
        return None


def update_entity(entity, new_value):
    try:
        entity.update(new_value)
    except:
        return None
