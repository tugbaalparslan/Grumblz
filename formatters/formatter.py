def format_user_to_json(user):
    return {
        "email": user.email,
        "name": user.name,
        "last_name": user.last_name,
        "password": user.password,
        "phone": user.phone,
        "gender": user.gender
    }


def format_company_to_json(company):
    return {
        "us_employer_id": company.us_employer_id,
        "company_name": company.company_name,
        "business_area": company.business_area,
        "number_of_employees": company.number_of_employees,
        "phone": company.phone,
        "address": company.address
    }
