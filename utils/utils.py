import re

INVALID_USERNAME = "Invalid type of username. Enter a valid email."
USER_EXISTS = "User already exists."
USER_ADDED = "User added successfully."
USER_ADDED_ERROR = "Error while adding user."
USER_NOT_FOUND = "User not found."
SIGN_UP_SUCCESSFUL = "Sign Up successful."

CANDIDATE_NOT_FOUND = "Candidate not found."
CANDIDATE_ADDED = "Candidate was added."
CANDIDATE_ADDED_ERROR = "Error while adding candidate"
CANDIDATE_UPDATED = "Candidate was updated."
CANDIDATE_UPDATED_ERROR = "Error while adding candidate"
CANDIDATE_DELETED = "Candidate was deleted."
CANDIDATE_DELETED_ERROR = "Error while deleting candidate"

AUTH_INVALID = "Invalid credentials. Please try again or sign up."

APP_TITLE = "Fast Api Assignment"
APP_DESCRIPTION = """
A Fast Api application to register as a user and enter candidates information.
"""


def is_valid_username(username: str) -> bool:
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.match(regex, username):
        return True
    else:
        return False