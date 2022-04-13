"""
To configure the connection string for Azure storage, go to https://docs.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string#configure-a-connection-string-for-an-azure-storage-account
Then, store the connection string as a Secret named AZURE_STORAGE_CONNECTION_STRING

Finally, create a blog container and set it as name e.g. "flows" blob container
"""
import platform
import prefect
from prefect import Flow, task
from prefect.storage import Azure
from prefect.run_configs import DockerRun


FLOW_NAME = "azure_docker_run_default_image"
STORAGE = Azure(
    container="flows", connection_string_secret="AZURE_STORAGE_CONNECTION_STRING",
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
    storage=STORAGE,
    run_config=DockerRun(labels=["docker"], image="prefecthq/prefect:1.0.0-python3.8"),
) as flow:
    hw = hello_world()
