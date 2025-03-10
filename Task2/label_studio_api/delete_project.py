import os
from label_studio_sdk import Client
from label_studio_config import LABEL_STUDIO_URL, API_KEY

def delete_project(project_id):
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    ls.delete_project(project_id)
    print(f"Project {project_id} deleted successfully.")

if __name__ == "__main__":
    # Always read project_id.txt from the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "project_id.txt")

    with open(file_path, "r") as f:
        project_id_str = f.read().strip()
    project_id = int(project_id_str)

    delete_project(project_id)
