"""
python flows/different_images_per_subflows/parent_docker_different_images_per_subflows.py
"""
import uuid
from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import DockerRun
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run
import subprocess

FLOW_NAME = "parent_docker_different_images_per_subflow"
AGENT_LABEL = "docker"
PREFECT_PROJECT_NAME = "community"
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
def hello_world():
    print(f"Hello from {FLOW_NAME}!")
    return FLOW_NAME


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    normal_non_subflow_task = hello_world()
    # === FIRST FLOW WITH PYTHON 3.9 DOCKER IMAGE ===
    first_child_flow_run_id = create_flow_run(
        flow_name="first_flow_docker",
        project_name=PREFECT_PROJECT_NAME,
        parameters=dict(user_input="first child flow"),
        run_config=DockerRun(
            labels=[AGENT_LABEL], image="prefecthq/prefect:1.0.0-python3.9"
        ),
        upstream_tasks=[normal_non_subflow_task],
    )
    first_child_flowrunview = wait_for_flow_run(
        first_child_flow_run_id, raise_final_state=True, stream_logs=True
    )
    # === SECOND FLOW WITH PYTHON 3.8 DOCKER IMAGE  ===
    second_child_flow_run_id = create_flow_run(
        flow_name="second_flow_docker",
        project_name=PREFECT_PROJECT_NAME,
        parameters=dict(user_input="second child flow"),
        run_config=DockerRun(
            labels=[AGENT_LABEL], image="prefecthq/prefect:1.0.0-python3.8"
        ),
        upstream_tasks=[first_child_flowrunview],
    )
    second_child_flowrunview = wait_for_flow_run(
        second_child_flow_run_id, raise_final_state=True, stream_logs=True
    )
    # === FIRST FLOW AGAIN BUT WITH PYTHON 3.7 DOCKER IMAGE  ===
    again_first_child_flow_run_id = create_flow_run(
        flow_name="first_flow_docker",
        project_name=PREFECT_PROJECT_NAME,
        parameters=dict(user_input="first child flow"),
        run_config=DockerRun(
            labels=[AGENT_LABEL], image="prefecthq/prefect:1.0.0-python3.7"
        ),
        # idempotency_key=str(uuid.uuid4()),
        upstream_tasks=[second_child_flowrunview],
    )
    first_child_flowrunview = wait_for_flow_run(
        again_first_child_flow_run_id, raise_final_state=True, stream_logs=True
    )
if __name__ == "__main__":
    subprocess.run(
        f"prefect register --project {PREFECT_PROJECT_NAME} -p flows/different_images_per_subflows/",
        shell=True,
    )
    subprocess.run(
        f"prefect run --name {FLOW_NAME} --project {PREFECT_PROJECT_NAME}", shell=True
    )
    subprocess.run(
        f"prefect agent docker start --label {AGENT_LABEL} --volume ~/.aws:/root/.aws",
        shell=True,
    )
