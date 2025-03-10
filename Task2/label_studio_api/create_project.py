import os
from label_studio_sdk import Client
from label_studio_config import LABEL_STUDIO_URL, API_KEY

def create_project():
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    label_config = """
    <View>
      <Image name="image" value="$image"/>
      <Choices name="choice" toName="image">
        <Choice value="Yes"/>
        <Choice value="No"/>
      </Choices>
    </View>
    """

    project = ls.start_project(
        title="MyTestProject",
        label_config=label_config
    )
    print(f"Project created with ID: {project.id}")
    return project.id
#The new project we create the id of that project gets stored in the txt file for later use
if __name__ == "__main__":
    project_id = create_project()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "project_id.txt")

    with open(file_path, "w") as f:
        f.write(str(project_id))
