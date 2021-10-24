from prefect import Flow, task
from prefect.storage import S3
from prefect.run_configs import KubernetesRun
from prefect.client.secrets import Secret
from prefect.tasks.kubernetes import RunNamespacedJob


FLOW_NAME = "s3_kubernetes_run_RunNamespacedJob"
AWS_ACCESS_KEY_ID = Secret("AWS_ACCESS_KEY_ID").get()
AWS_SECRET_ACCESS_KEY = Secret("AWS_SECRET_ACCESS_KEY").get()
STORAGE = S3(
    bucket="prefect-datasets",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    local_script_path=f"flows_task_library/{FLOW_NAME}.py",
)


body = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {"name": "dummy"},
    "spec": {
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "echo",
                        "image": "alpine:3.7",
                        "command": ["echo", "Hello"],
                    }
                ],
                "restartPolicy": "Never",
            }
        },
        "backoffLimit": 4,
    },
}
k8s_job = RunNamespacedJob(body=body, kubernetes_api_key_secret=None)


with Flow(
    FLOW_NAME,
    storage=STORAGE,
    run_config=KubernetesRun(
        labels=["k8s"],
        env={
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        },
    ),
) as flow:
    k8s_job()
