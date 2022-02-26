"""
In order ti successfully upload the flow script file to GCS on flow registration,
you need to have this env variable set in your local environment:
export GOOGLE_APPLICATION_CREDENTIALS="/Users/anna/repos/packaging-prefect-flows/gcs_sa.json"
- adjust the above oath to your service account JSON path

To see how to generate this file, see: https://cloud.google.com/docs/authentication/getting-started

To start an agent for this flow:
prefect agent local start --label gcs_local --no-hostname-label

From another terminal:
prefect register --project community -p flows/gcs_flow_of_flows_local_run/

Then:
prefect run --name gcs_parent_local --project community --watch
"""
from prefect import Flow, task
from prefect.storage import GCS
from prefect.run_configs import LocalRun
from prefect.tasks.prefect import create_flow_run
import uuid

FLOW_NAME = "gcs_parent_local"
AGENT_LABEL = "gcs_local"
STORAGE = GCS(
    bucket="prefect-community",
    key=f"flows/gcs_flow_of_flows_local_run/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/gcs_flow_of_flows_local_run/{FLOW_NAME}.py",
)

RUN_CONFIG = LocalRun(labels=[AGENT_LABEL],)


@task(log_stdout=True)
def hello_world():
    print(f"Hello from {FLOW_NAME}!")
    return FLOW_NAME


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()
    create_flow_run(
        flow_name="gcs_child_local",
        project_name="community",
        parameters=dict(user_input=hw),
        idempotency_key=str(uuid.uuid4()),
    )

if __name__ == "__main__":
    flow.visualize()
