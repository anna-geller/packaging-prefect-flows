"""
First, login to the registry:
az acr login --name prefectcommunity

Make sure your custom module is installed within your registration environment:
pip install .

Then, register the flow:
prefect register --project community -p flows/docker_pickle_docker_run_acr_image.py
"""
from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import DockerRun


FLOW_NAME = "docker_pickle_docker_run_acr_image_no_dockerfile"
REGISTRY_URL = "prefectcommunity.azurecr.io/images/"
docker_storage = Docker(
    base_image="prefecthq/prefect:1.0.0-python3.8",
    image_name=FLOW_NAME,
    image_tag="latest",
    python_dependencies=["pandas", "awswrangler"],
    registry_url=REGISTRY_URL,
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from a new Azure VM after a reboot and with long-lived ACR permissions!"
    print(text)
    # the imports below are only to demonstrate that custom modules were installed in the image
    import pandas
    import awswrangler
    print("printing package versions")
    print(pandas.__version__)
    print(awswrangler.__version__)
    return text


with Flow(
    FLOW_NAME,
    storage=docker_storage,
    run_config=DockerRun(
        image=f"{REGISTRY_URL}{FLOW_NAME}:latest",
        labels=["docker"],
    ),
) as flow:
    hw = hello_world()
