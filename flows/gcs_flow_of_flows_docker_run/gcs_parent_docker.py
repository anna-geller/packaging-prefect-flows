"""
In order to successfully upload the flow script file to GCS on flow registration,
you need to have this env variable set in your local environment:
export GOOGLE_APPLICATION_CREDENTIALS="/Users/yourname/path/to/your/repo/packaging-prefect-flows/gcs_sa.json"
- adjust the above oath to your service account JSON path

To see how to generate this file, see: https://cloud.google.com/docs/authentication/getting-started

To register this flow and the corresponding child flow,
export the GOOGLE_APPLICATION_CREDENTIALS env variable and run this python script, e.g.:
    export GOOGLE_APPLICATION_CREDENTIALS="/Users/anna/repos/packaging-prefect-flows/gcs_sa.json"
    python flows/gcs_flow_of_flows_docker_run/gcs_parent_docker.py
"""
from prefect import Flow, task
from prefect.storage import GCS
from prefect.run_configs import DockerRun
from prefect.tasks.prefect import create_flow_run
import subprocess
import uuid

FLOW_NAME = "gcs_parent_docker"
AGENT_LABEL = "gcs_docker"
GCS_SA_PATH = "/Users/anna/repos/packaging-prefect-flows/gcs_sa.json"
PREFECT_PROJECT_NAME = "community"
STORAGE = GCS(
    bucket="prefect-community",
    key=f"flows/gcs_flow_of_flows_docker_run/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/gcs_flow_of_flows_docker_run/{FLOW_NAME}.py",
)

RUN_CONFIG = DockerRun(labels=[AGENT_LABEL],)


@task(log_stdout=True)
def hello_world():
    print(f"Hello from {FLOW_NAME}!")
    return FLOW_NAME


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()
    create_flow_run(
        flow_name="gcs_child_docker",
        project_name=PREFECT_PROJECT_NAME,
        parameters=dict(user_input=hw),
        idempotency_key=str(uuid.uuid4()),
    )

if __name__ == "__main__":
    subprocess.run(
        f"prefect register --project {PREFECT_PROJECT_NAME} -p flows/gcs_flow_of_flows_docker_run/",
        shell=True,
    )
    subprocess.run(
        f"prefect run --name {FLOW_NAME} --project {PREFECT_PROJECT_NAME}", shell=True
    )
    subprocess.run(
        f'prefect agent docker start --label {AGENT_LABEL} --volume {GCS_SA_PATH}:/opt/prefect/gcs_sa.json --env GOOGLE_APPLICATION_CREDENTIALS="/opt/prefect/gcs_sa.json"',
        shell=True,
    )
