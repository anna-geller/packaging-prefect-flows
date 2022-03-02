from prefect import Flow, task
from prefect.storage import S3
from prefect.run_configs import KubernetesRun
from prefect.client.secrets import Secret

# the import below is only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query

AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "s3_kubernetes_run_custom_ecr_image"
STORAGE = S3(
    bucket="prefect-datasets",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    # if you add local_script_path, Prefect will upload the local Flow script to S3 during registration
    local_script_path=f"flows/{FLOW_NAME}.py",
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME}"
    print(text)
    return text


with Flow(
    FLOW_NAME,
    storage=STORAGE,
    run_config=KubernetesRun(
        image=f"{AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com/community:latest",
        labels=["k8s"],
        image_pull_secrets=["aws-ecr-secret"],
    ),
) as flow:
    hw = hello_world()
