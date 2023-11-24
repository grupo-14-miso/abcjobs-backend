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

def get_candidates_ready(candidates, assignments, candidates_on_pre_interview, required_complete_assignments):
    candidates_ready = []
    for candidate in candidates:
        candidate_completed_assignments = []
        for assignment in assignments:
            assignment_candidate = assignment.get('candidate')
            status = assignment.get('status')
            assignment_type = assignment.get('type')
            if assignment_candidate == str(candidate.id) and str(candidate.id) in candidates_on_pre_interview and status == 'finished' and assignment_type \
                    not in candidate_completed_assignments and assignment_type in required_complete_assignments:
                candidate_completed_assignments.append(assignment_type)
        if len(candidate_completed_assignments) >= 3:
            candidates_ready.append({
            "id": candidate.id,
            "id_candidato": candidate.get('id_candidato'),
            "name": candidate.get('Nombre', '') + candidate.get('apellido', '')
        })
    return candidates_ready


def update_entity(entity, new_value):
    try:
        entity.update(new_value)
    except:
        return None
