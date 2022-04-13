"""
First, login to the registry:
az acr login --name prefectcommunity

Make sure your custom module is installed within your registration environment:
pip install .

Then, register the flow:
prefect register --project azure -p flows/docker_pickle_docker_run_acr_image.py
"""
import platform
import prefect
from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import DockerRun

# the import below is only to demonstrate that custom modules were installed in the image
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "docker_pickle_docker_run_acr_image"
docker_storage = Docker(
    image_name=FLOW_NAME,
    image_tag="latest",
    registry_url="prefectcommunity.azurecr.io/images/",
    dockerfile="/Users/anna/repos/packaging-prefect-flows/Dockerfile",
)


@task(log_stdout=True)
def hello_world():
    logger = prefect.context.get("logger")
    logger.info("Hello from %s", FLOW_NAME)
    logger.info(
        "Platform information: IP = %s, Python = %s, Platform type = %s, OS Version = %s",
        platform.node(),
        platform.python_version(),
        platform.platform(),
        platform.version(),
    )


with Flow(
    FLOW_NAME,
    storage=docker_storage,
    run_config=DockerRun(
        image=f"prefectcommunity.azurecr.io/images/{FLOW_NAME}:latest",
        labels=["docker"],
    ),
) as flow:
    hw = hello_world()
