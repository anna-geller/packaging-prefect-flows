"""
To use flow script files in Docker, we need the following arguments to be set properly:
- `stored_as_script` = True
- `path` must point to the path in the image
- if this path is different than /opt/prefect/flows/YOUR_FLOW.py,
  then you also need to change the default `prefect_directory` to your custom directory
- you need to add the flow to the storage explicitly before registering, e.g.: docker_storage.add_flow(flow)
- finally, registering the flow must happen from Python, since the `prefect register` CLI doesn't have the option
  to pass build=False, and this is critical to include to prevent pickling flow and rebuilding the image on registration
- the parameter `ignore_healthchecks` on the Docker storage is optional and doesn't affect this process at all
"""
from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import KubernetesRun

# the import below are only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "docker_script_kubernetes_run_custom_ecr_image"
docker_storage = Docker(
    image_name="community",
    image_tag="latest",
    registry_url="123456789.dkr.ecr.eu-central-1.amazonaws.com",
    stored_as_script=True,
    path=f"/opt/prefect/flows/{FLOW_NAME}.py",
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME}"
    print(text)
    return text


with Flow(
    FLOW_NAME,
    storage=docker_storage,
    run_config=KubernetesRun(
        image="123456789.dkr.ecr.eu-central-1.amazonaws.com/community:latest",
        labels=["k8s"],
        image_pull_secrets=["aws-ecr-secret"],
    ),
) as flow:
    hw = hello_world()

if __name__ == "__main__":
    docker_storage.add_flow(flow)
    flow.register(project_name="community", build=False)
