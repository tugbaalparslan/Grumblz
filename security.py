from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(email, password):
    # this is the method where we will compare the username with stored password.
    # if it succeeds, it will return JWT token to the client. Client will use this token for the next requests it makes
    # for security purposes.
    # identity method below will check if the sent JW token is a valid one.
    found_user = UserModel.find_by_email(email)

    if found_user and safe_str_cmp(found_user.password, password):
        return found_user


# identity method extracts user id from the JW token sent with the request by client to see if the user id is valid.
# so the request it made will be processed
def identity(payload):
    user_id = payload['identity']
    found_user = UserModel.find_by_id(user_id)
    return found_user
