"""
To use local storage with DockerRun (and Docker agent), we need to:
- set `stored_as_script=True`
- provide a path on container, rather than on a local disk
- ensure to `add_default_labels=False` otherwise the host name of the Local storage will be added to the labels,
    causing that the flow will not match with the Docker agent
"""
from prefect import Flow, task
from prefect.storage import Local
from prefect.run_configs import DockerRun

# the import below is only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "docker_script_docker_run_local_image"
storage = Local(
    path=f"/opt/prefect/flows/{FLOW_NAME}.py",
    stored_as_script=True,
    add_default_labels=False,
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME}"
    print(text)
    return text


with Flow(
    FLOW_NAME,
    storage=storage,
    run_config=DockerRun(image="community:latest", labels=["docker"],),
) as flow:
    hw = hello_world()
