def get_schema():
    return """
    users(id, email)
    projects(id, user_id, name)
    tasks(id, user_id, project_id, content)
    """