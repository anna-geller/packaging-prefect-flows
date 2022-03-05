"""
Usage:
cd flows/ && prefect register --project xyz -p s3_ecs_run_task_definition_as_dict_incl_logging_options.py
prefect run --name s3_ecs_run_task_definition_as_dict_incl_logging_options --watch
"""
import prefect
from prefect.storage import S3
from prefect.run_configs import ECSRun
from prefect import task, Flow
from prefect.client.secrets import Secret


FLOW_NAME = "s3_ecs_run_task_definition_as_dict_incl_logging_options"
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
                image="prefecthq/prefect:1.0.0-python3.8",
                logConfiguration={
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": f"{FLOW_NAME}_logs",
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs",
                        "awslogs-create-group": "true",
                    },
                },
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
