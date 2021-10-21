from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import KubernetesRun

# the import below are only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "docker_pickle_kubernetes_run_custom_ecr_image"
docker_storage = Docker(
    image_name="community",
    image_tag="latest",
    registry_url="123456789.dkr.ecr.eu-central-1.amazonaws.com",
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
        image="123456789.dkr.ecr.eu-central-1.amazonaws.com/community:latest",
        labels=["k8s"],
        image_pull_secrets=["aws-ecr-secret"],
    ),
) as flow:
    hw = hello_world()

if __name__ == "__main__":
    flow.register(project_name="community", build=True)
