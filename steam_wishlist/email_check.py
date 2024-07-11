def check_struct_email(user_email: str) -> bool:
    structure_email = "@gmail.com"
    if structure_email in user_email:
        return True
    return False