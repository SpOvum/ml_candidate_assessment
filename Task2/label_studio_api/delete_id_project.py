# delete_project.py
from label_studio_sdk import Client
from label_studio_config import LABEL_STUDIO_URL, API_KEY

def delete_project(project_id):
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    ls.delete_project(project_id)
    print(f"Project {project_id} deleted successfully.")

if __name__ == "__main__":
    #to delete a particular project
    project_id = 3
    delete_project(project_id)