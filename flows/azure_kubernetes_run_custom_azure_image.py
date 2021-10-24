from prefect import Flow, task
from prefect.storage import Azure
from prefect.run_configs import KubernetesRun
# the import below are only to demonstrate that custom modules were installed in the ECR image "community"
from flow_utilities.db import get_df_from_sql_query


FLOW_NAME = "azure_kubernetes_run_custom_azure_image"
STORAGE = Azure(
    container="flows",
    connection_string_secret="AZURE_STORAGE_CONNECTION_STRING",
    # storing as script with Azure would require uploading the file beforehand e.g. as part of CI/CD
    # stored_as_script=True,
    # blob_name=f"flows/{FLOW_NAME}.py",
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
        image="prefectdemos.azurecr.io/community/flows",
        labels=["aks"],
        image_pull_secrets=["aks"],  # see README
    ),
) as flow:
    hw = hello_world()
