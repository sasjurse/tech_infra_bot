def retrieve_current_plan():
    path = '../project_descriptions/version 1'
    with open(path, 'r') as f:
        return f.read()