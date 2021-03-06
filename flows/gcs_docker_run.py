"""
In order ti successfully upload the flow script file to GCS on flow registration,
you need to have this env variable set in your local environment:
export GOOGLE_APPLICATION_CREDENTIALS="/Users/anna/repos/packaging-prefect-flows/gcs_sa.json"
- adjust the above oath to your service account JSON path

To see how to generate this file, see: https://cloud.google.com/docs/authentication/getting-started
"""
from prefect import Flow, task
from prefect.storage import GCS
from prefect.run_configs import DockerRun
import subprocess


FLOW_NAME = "gcs_docker_run"
AGENT_LABEL = "docker"
GCS_SA_PATH = "/Users/anna/repos/packaging-prefect-flows/gcs_sa.json"
STORAGE = GCS(
    bucket="prefect-community",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/{FLOW_NAME}.py",
)

RUN_CONFIG = DockerRun(labels=[AGENT_LABEL],)


@task(log_stdout=True)
def hello_world():
    print(f"Hello from {FLOW_NAME}!")


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()

if __name__ == "__main__":
    flow_id = flow.register("community")
    subprocess.run(f"prefect run --id {flow_id}", shell=True)
    subprocess.run(
            f'prefect agent docker start --label {AGENT_LABEL} --volume {GCS_SA_PATH}:/opt/prefect/gcs_sa.json --env GOOGLE_APPLICATION_CREDENTIALS="/opt/prefect/gcs_sa.json"',
            shell=True,
        )
