def is_admin(user_id):
    """
    This function opens admin_list.txt file
    Then returns 1 if id is in the file (is admin)
    Returns 0 otherwise
    """
    with open('data/admin_list.txt', 'r') as file:
        if str(user_id) in file.read():
            return 1
    return 0


def bot_owner():
    with open('data/admin_list.txt', 'r') as file:
        return file.readline().rstrip()
