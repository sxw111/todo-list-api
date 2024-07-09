def http_400_username_details(username: str) -> str:
    return f"User with username `{username}` arleady exist!"


def http_400_email_details(email: str) -> str:
    return f"User with email `{email}` arleady exist!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed!"


def http_404_id_details(user_id: int) -> str:
    return f"User with id `{user_id}` does not exist!"


def http_404_todo_id_details(todo_id: int) -> str:
    return f"Todo with id {todo_id} does not exist!"


def http_404_todos_details() -> str:
    return f"Currently, you don't have any todos!"


def http_403_access_denied_details() -> str:
    return "You do not have permission to perform this action!"
