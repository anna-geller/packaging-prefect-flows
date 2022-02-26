"""
In order ti successfully upload the flow script file to GCS on flow registration,
you need to have this env variable set in your local environment:
export GOOGLE_APPLICATION_CREDENTIALS="/Users/anna/repos/packaging-prefect-flows/gcs_sa.json"
- adjust the above oath to your service account JSON path

To see how to generate this file, see: https://cloud.google.com/docs/authentication/getting-started

To register and run this flow from a parent flow,
check the file: flows/gcs_flow_of_flows_docker_run/gcs_parent_docker.py
"""
from prefect import Flow, Parameter, task
from prefect.storage import GCS
from prefect.run_configs import DockerRun


FLOW_NAME = "gcs_child_docker"
AGENT_LABEL = "gcs_docker"
STORAGE = GCS(
    bucket="prefect-community",
    key=f"flows/gcs_flow_of_flows_docker_run/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/gcs_flow_of_flows_docker_run/{FLOW_NAME}.py",
)

RUN_CONFIG = DockerRun(labels=[AGENT_LABEL],)


@task(log_stdout=True)
def hello_world(x: str):
    print(f"Hello {x} from {FLOW_NAME}!")


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    user_input = Parameter("user_input", default="world")
    hw = hello_world(user_input)
