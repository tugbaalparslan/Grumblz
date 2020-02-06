from models.user import UserModel
from werkzeug.security import safe_str_cmp


# authenticate if the email + password matches the one stored in DB. This is the part where the JW Token is created
# if login is successful. JWT is sent back to the client. Client will use this token for future requests to prove
# it has logged in already. If login is not successful, returns HTTP 401 - Unauthorized status code.
def authenticate(user_email, password):
    # this is the method where we will compare the username with stored password.
    # if it succeeds, it will return JWT token to the client. Client will use this token for the next requests it makes
    # for security purposes.
    # identity method below will check if the sent JW token is a valid one.
    found_user = UserModel.find_by_email(user_email)

    if found_user and safe_str_cmp(found_user.password, password):
        return found_user


# identity method extracts user id from the JW token sent with the request by client to see if the token and
# the user id is valid. If so the request will be processed. Otherwise won't. (Throws 401 Err Code if not valid or
# the token signature is expired) This is the authorization part.
def identity(payload):
    user_id = payload['identity']
    found_user = UserModel.find_by_id(user_id)
    return found_user
