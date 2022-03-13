import prefect
from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import ECSRun


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_ecs_run_pr_example"
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"{FLOW_NAME}.py",
)

RUN_CONFIG = ECSRun(
    labels=["ecs-agent-local"], image="prefecthq/prefect:1.1.0-python3.7"
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    return text


with Flow(FLOW_NAME, run_config=RUN_CONFIG, storage=STORAGE) as flow:
    hello_world()
