import prefect
from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import ECSRun


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_ecs_run_fargate_spot"
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/{FLOW_NAME}.py",
)

RUN_CONFIG = ECSRun(
    labels=["prod"],
    task_role_arn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/prefectTaskRole",  # a role with S3 permissions
    run_task_kwargs=dict(
        cluster="prefectEcsCluster",
        # platformVersion="1.3.0",
        capacityProviderStrategy=[
            {"capacityProvider": "FARGATE_SPOT", "weight": 1, "base": 0},
        ],
    ),
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    return text


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()
