from google.cloud import datastore


def get_entities_by_field(entity, field_name, field_value):
    # Initialize the Datastore client
    client = datastore.Client()

    # Query all Users
    query = client.query(kind=entity).add_filter(field_name, '=', field_value)
    results = list(query.fetch())
    try:
        return results
    except:
        return None