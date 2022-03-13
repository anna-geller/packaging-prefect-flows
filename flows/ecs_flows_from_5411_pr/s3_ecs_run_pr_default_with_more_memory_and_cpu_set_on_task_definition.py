import prefect
from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import ECSRun


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_ecs_run_pr_default_with_more_memory_and_cpu_set_on_task_definition"
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"{FLOW_NAME}.py",
)

RUN_CONFIG = ECSRun(
    labels=["ecs-agent-local"],
    task_definition=dict(
        family=FLOW_NAME,
        requiresCompatibilities=["FARGATE"],
        networkMode="awsvpc",
        cpu=4096,
        memory=9216,  # default for this CPU value is 8192 - in 1024 increments,
        taskRoleArn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/prefectTaskRole",
        executionRoleArn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/prefectECSAgentTaskExecutionRole",
        containerDefinitions=[
            dict(name="flow", image="prefecthq/prefect:1.1.0-python3.9",)
        ],
    ),
    run_task_kwargs=dict(cluster="prefectEcsCluster"),
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    import platform

    print(f"Python version: {platform.python_version()}")
    return text


with Flow(FLOW_NAME, run_config=RUN_CONFIG, storage=STORAGE) as flow:
    hello_world()
