from prefect import Flow, task
from prefect.storage import GitHub
from prefect.run_configs import KubernetesRun
# the import below are only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "github_kubernetes_run_custom_ecr_image"
STORAGE = GitHub(
    repo="anna-geller/packaging-prefect-flows",
    path=f"flows/{FLOW_NAME}.py",
    access_token_secret="GITHUB_ACCESS_TOKEN",  # required with private repositories
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
            image="123456789.dkr.ecr.eu-central-1.amazonaws.com/community:latest",
            labels=["k8s"],
            image_pull_secrets=["aws-ecr-secret"]  # see README
        ),
) as flow:
    hw = hello_world()

if __name__ == "__main__":
    flow.register(project_name="community")
