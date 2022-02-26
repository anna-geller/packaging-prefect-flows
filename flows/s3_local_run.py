from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import LocalRun
import subprocess


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_local_run"
AGENT_LABEL = "dev"
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/{FLOW_NAME}.py",
)

RUN_CONFIG = LocalRun(labels=[AGENT_LABEL],)


@task(log_stdout=True)
def hello_world():
    print("Hello world!")


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()

if __name__ == "__main__":
    flow_id = flow.register("community")
    subprocess.run(f"prefect run --id {flow_id}", shell=True)
    subprocess.run(
        f"prefect agent local start --label {AGENT_LABEL} --no-hostname-label",
        shell=True,
    )
