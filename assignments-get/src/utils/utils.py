def get_assignments_to_return(client, pre_interview_entities):
    assignments_to_return = []

    for pre_interview_entity in pre_interview_entities:
        id_candidate = pre_interview_entity['id_candidate']

        assigment_query = client.query(kind='assignments-data')
        assigment_query.add_filter('candidate', '=', id_candidate)
        assigment_query.add_filter('type', '=', 'Performance')

        assignments = list(assigment_query.fetch())
        for assignment in assignments:
            key_candidate = client.key('candidates', int(id_candidate))
            candidate = client.get(key_candidate)
            if candidate:
                assignment_data = {
                    'assignment_id': assignment.key.id,
                    'rol': assignment['rol'],
                    'type': assignment['type'],
                    'focus': assignment['focus'],
                    'questions': assignment['questions'],
                    'status': assignment['status'],
                    'result': assignment['result'],
                    'nombre': candidate['Nombre'],
                    'apellido': candidate['apellido']
                }
                assignments_to_return.append(assignment_data)
    return assignments_to_return
