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


FLOW_NAME = "docker_pickle_docker_run_acr_image_no_dockerfile"
REGISTRY_URL = "prefectcommunity.azurecr.io/images/"
docker_storage = Docker(
    # base_image="prefecthq/prefect:1.0.0-python3.8",
    image_name=FLOW_NAME,
    image_tag="latest",
    python_dependencies=["pandas", "awswrangler"],
    registry_url=REGISTRY_URL,
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
    # the imports below are only to demonstrate that custom modules were installed in the image
    import pandas
    import awswrangler

    logger.info(
        "printing package versions - pandas %, awswrangler: %s",
        pandas.__version__,
        awswrangler.__version__,
    )


with Flow(
    FLOW_NAME,
    storage=docker_storage,
    run_config=DockerRun(image=f"{REGISTRY_URL}{FLOW_NAME}:latest", labels=["docker"],),
) as flow:
    hw = hello_world()
