pre_interview_domain = 'pre_interview'
candidates_domain = 'candidates'
interviews_domain = 'interviews'
offers_data_domain = 'offers-data'
companies_data_domain = 'companies-data'


def remove_password_properties(entity):
    if 'password_hash' and 'salt' in entity:
        del entity['password_hash']
        del entity['salt']
    return entity


def get_details_for_interview(client, interview_entity):
    candidate_details = []
    for candidate_id in interview_entity['candidates']:
        # Fetch details from candidates entity
        candidate_key = client.key(candidates_domain, int(candidate_id))
        candidate_entity = client.get(candidate_key)
        remove_password_properties(candidate_entity)

        # Fetch details from offers-data entity
        offer_key = client.key(offers_data_domain, int(interview_entity['id_offer']))
        offer_entity = client.get(offer_key)

        # Fetch details from companies-data entity
        company_key = client.key(companies_data_domain, int(interview_entity['id_company']))
        company_entity = client.get(company_key)
        remove_password_properties(company_entity)

        # Combine all details
        candidate_details.append({
            'candidate': candidate_entity,
            'offer': offer_entity,
            'company': company_entity,
        })
    return candidate_details
