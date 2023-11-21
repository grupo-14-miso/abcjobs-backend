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


def get_entities_by_field(entity, field_name, field_value):
    # Initialize the Datastore client
    client = datastore.Client()
    # Query all Users
    query = client.query(kind=entity).add_filter(field_name, '=', field_value)
    try:
        return list(query.fetch())
    except:
        return []


def get_results_from_entity(entity):
    # Initialize the Datastore client
    client = datastore.Client()
    # Query all results
    query = client.query(kind=entity)
    results = query.fetch()
    return list(results)


def update_entity(entity, new_value):
    try:
        entity.update(new_value)
    except:
        return None
