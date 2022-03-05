import platform
import prefect
from prefect import Flow, Parameter, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import DockerRun
import subprocess

PREFECT_PROJECT_NAME = "community"
FLOW_NAME = "s3_docker_run_local_image"
AGENT_LABEL = "docker"
AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"{FLOW_NAME}.py",
)

RUN_CONFIG = DockerRun(labels=[AGENT_LABEL],)


@task(log_stdout=True)
def hello_world(x: str):
    print(f"Hello {x} from {FLOW_NAME}!")
    print(
        f"Running this task with Prefect: {prefect.__version__} and Python {platform.python_version()}"
    )


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    user_input = Parameter("user_input", default="Marvin")
    hw = hello_world(user_input)

if __name__ == "__main__":
    subprocess.run(
        f"prefect register --project {PREFECT_PROJECT_NAME} -p flows/s3_docker_run_local_image.py",
        shell=True,
    )
    subprocess.run(
        f"prefect run --name {FLOW_NAME} --project {PREFECT_PROJECT_NAME}", shell=True
    )
    subprocess.run(
        f'prefect agent docker start --label {AGENT_LABEL} --volume ~/.aws:/root/.aws"',
        shell=True,
    )
