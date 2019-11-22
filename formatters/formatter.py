def format_user_to_json(user):
    return {
        "email": user.email,
        "name": user.name,
        "last_name": user.last_name,
        "phone": user.phone,
        "gender": user.gender
    }