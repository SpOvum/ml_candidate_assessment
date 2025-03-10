import os
import json
from label_studio_sdk import Client
from label_studio_config import LABEL_STUDIO_URL, API_KEY

def export_data(project_id):
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    project = ls.get_project(project_id)

    exported = project.export_tasks()
    print("Exported project data:")
    print(exported)
    return exported

if __name__ == "__main__":
    # Always read project_id.txt from the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "project_id.txt")

    with open(file_path, "r") as f:
        project_id_str = f.read().strip()
    project_id = int(project_id_str)

    data = export_data(project_id)

    # Optionally save the data to a JSON file in the same folder
    exported_file_path = os.path.join(script_dir, "exported_data.json")
    with open(exported_file_path, "w") as f:
        json.dump(data, f, indent=2)
