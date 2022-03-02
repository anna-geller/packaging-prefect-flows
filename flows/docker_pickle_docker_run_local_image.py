from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import DockerRun

# the import below is only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "docker_pickle_docker_run_local_image"
docker_storage = Docker(
    image_name="community",
    image_tag="latest",
    dockerfile="/Users/anna/repos/packaging-prefect-flows/Dockerfile",
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME}"
    print(text)
    return text


with Flow(
    FLOW_NAME,
    storage=docker_storage,
    run_config=DockerRun(image="community:latest", labels=["docker"],),
) as flow:
    hw = hello_world()
