"""
Within the JSON file "prefect_flow_task_definition.json",
make sure to replace the AWS account ID 123456789 by your Account ID!
Then register it using this command:
    aws ecs register-task-definition --cli-input-json file://prefect_flow_task_definition.json
Or if you use a YAML file instead such as in `flow_task_definition.yaml` in this folder:
    aws ecs register-task-definition --cli-input-yaml file://flow_task_definition.yaml
Then, you can reference it in "task_definition_arn" using "family:revision"
"""
import prefect
from prefect import Flow, task
from prefect.client.secrets import Secret
from prefect.storage import S3
from prefect.run_configs import ECSRun
import flow_utilities  # to validate that custom image works


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_ecs_run_preregistered_task_definition"
STORAGE = S3(
    bucket="prefectdata",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # this will ensure to upload the Flow script to S3 during registration
    local_script_path=f"flows/{FLOW_NAME}.py",
)

RUN_CONFIG = ECSRun(
    labels=["prod"],
    task_definition_arn="prefectFlow:1",
    run_task_kwargs=dict(cluster="prefectEcsCluster"),
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    return text


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()
