from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import KubernetesRun
from prefect.client.secrets import Secret

# the import below are only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


AWS_ACCOUNT_ID = Secret("AWS_ACCOUNT_ID").get()
FLOW_NAME = "docker_pickle_kubernetes_run_custom_ecr_image"
docker_storage = Docker(
    image_name="community",
    image_tag="latest",
    registry_url=f"{AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com",
    dockerfile="/Users/anna/repos/packaging-prefect-flows/Dockerfile",
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME}"
    print(text)
    return text


with Flow(
    FLOW_NAME,
    storage=docker_storage,
    run_config=KubernetesRun(
        image=f"{AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com/community:latest",
        labels=["k8s"],
        image_pull_secrets=["aws-ecr-secret"],
    ),
) as flow:
    hw = hello_world()
