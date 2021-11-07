import prefect
from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import ECSRun
import flow_utilities  # to validate that custom image works


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_ecs_run_custom_ecr_image"
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/{FLOW_NAME}.py",
)

RUN_CONFIG = ECSRun(
    labels=["prod"],
    image=f"{AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/community:latest",
    task_role_arn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/prefectTaskRole",  # S3 access
    execution_role_arn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/prefectECSAgentTaskExecutionRole",  # ECR access
    run_task_kwargs=dict(cluster="prefectEcsCluster"),
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    return text


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()
