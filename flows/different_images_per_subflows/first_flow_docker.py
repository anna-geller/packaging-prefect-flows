import platform
import prefect
from prefect import Flow, Parameter, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import DockerRun


FLOW_NAME = "first_flow_docker"
AGENT_LABEL = "docker"
AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/different_images_per_subflows/{FLOW_NAME}.py",
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
