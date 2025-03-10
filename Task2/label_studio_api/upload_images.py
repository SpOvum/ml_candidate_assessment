import os
from label_studio_sdk import Client
from label_studio_config import LABEL_STUDIO_URL, API_KEY

def upload_images(project_id):
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    project = ls.get_project(project_id)

    # Example tasks: replace these URLs with real images or local file paths
    tasks = [
        {"data": {"image": "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg"}},
        {"data": {"image": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Peacock_in_Indian_terai.jpg"}},
        {"data": {"image": "https://placekitten.com/200/300"}},
        {"data": {"image": "https://picsum.photos/id/237/200/300"}}
    ]

    project.import_tasks(tasks)
    print(f"Imported {len(tasks)} tasks into project {project_id}.")

if __name__ == "__main__":
    # Always read project_id.txt from the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "project_id.txt")

    with open(file_path, "r") as f:
        project_id_str = f.read().strip()
    project_id = int(project_id_str)

    upload_images(project_id)

