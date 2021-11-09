import prefect
from prefect.storage import S3
from prefect.run_configs import ECSRun
from prefect import task, Flow
from prefect.client.secrets import Secret


FLOW_NAME = "ecs_demo_ecr"
ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
STORAGE = S3(
    bucket="prefect-datasets",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    local_script_path=f"{FLOW_NAME}.py",
)
RUN_CONFIG = ECSRun(
    labels=["prod"],
    task_definition=dict(
        family=FLOW_NAME,
        requiresCompatibilities=["FARGATE"],
        networkMode="awsvpc",
        cpu=1024,
        memory=2048,
        taskRoleArn=f"arn:aws:iam::{ACCOUNT_ID}:role/prefectTaskRole",
        executionRoleArn=f"arn:aws:iam::{ACCOUNT_ID}:role/prefectECSAgentTaskExecutionRole",
        containerDefinitions=[
            dict(
                name="flow",
                image=f"{ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/community:latest",
            )
        ],
    ),
    run_task_kwargs=dict(cluster="prefectEcsCluster"),
)


@task
def say_hi():
    logger = prefect.context.get("logger")
    logger.info("Hi from Prefect %s from flow %s", prefect.__version__, FLOW_NAME)
    return


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    say_hi()
