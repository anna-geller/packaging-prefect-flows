"""
The example contents of .env file in this root project dir (.env file is obviously not committed):
ENV_1=value_1
ENV_2=value_2

Usage in CLI:
prefect agent docker start -l local_docker
prefect register --project xyz -p flows/docker_pickle_docker_run_envfile_example.py
prefect run --name docker_pickle_docker_run_envfile_example --watch
"""
import os
from dotenv import dotenv_values
from prefect import Flow, task
from prefect.run_configs import DockerRun
from prefect.storage import Docker

# Note: those env vars are read from root project dir and loaded to run config "env" at flow registration time
CONFIG = dotenv_values(".env")

FLOW_NAME = "docker_pickle_docker_run_envfile_example"
DOCKER_STORAGE = Docker(
    image_name=FLOW_NAME, image_tag="latest", python_dependencies=["python-dotenv"],
)


@task(log_stdout=True)
def print_env_vars_from_env_file():
    env1 = os.environ.get("ENV_1")
    env2 = os.environ.get("ENV_2")
    print(env1)
    print(env2)


with Flow(
    FLOW_NAME,
    run_config=DockerRun(
        image=f"{FLOW_NAME}:latest", labels=["local_docker"], env=CONFIG
    ),
    storage=DOCKER_STORAGE,
) as flow:
    print_env_vars_from_env_file()
