from prefect import Flow, task
from prefect.storage import S3
from prefect.run_configs import KubernetesRun
from prefect.client.secrets import Secret
from prefect.engine.signals import VALIDATIONFAIL
from prefect.triggers import all_finished
from prefect.tasks.kubernetes import (
    RunNamespacedJob,
    ReadNamespacedPodLogs,
    ListNamespacedPod,
    DeleteNamespacedPod,
    DeleteNamespacedJob,
)


FLOW_NAME = "s3_kubernetes_run_RunNamespacedJob_and_get_logs"
AWS_ACCESS_KEY_ID = Secret("AWS_ACCESS_KEY_ID").get()
AWS_SECRET_ACCESS_KEY = Secret("AWS_SECRET_ACCESS_KEY").get()
STORAGE = S3(
    bucket="prefect-datasets",
    key=f"flows/{FLOW_NAME}.py",
    stored_as_script=True,
    local_script_path=f"flows_task_library/{FLOW_NAME}.py",
)
JOB_NAME = "dummy"

body = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {"name": JOB_NAME},
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

delete_if_exists = DeleteNamespacedJob(
    job_name=JOB_NAME, kubernetes_api_key_secret=None
)
create_and_run_job = RunNamespacedJob(
    body=body,
    delete_job_after_completion=False,
    kubernetes_api_key_secret=None,
    trigger=all_finished,
)
list_pods = ListNamespacedPod(kubernetes_api_key_secret=None)
logs = ReadNamespacedPodLogs(kubernetes_api_key_secret=None)
delete_pod = DeleteNamespacedPod(kubernetes_api_key_secret=None)


@task(log_stdout=True)
def get_pod_ids(api_response):
    list_of_pods = []
    for i in api_response.items:
        list_of_pods.append(i.metadata.name)
    print(list_of_pods)
    return list_of_pods


@task(log_stdout=True)
def get_our_pod_name(pods):
    dummy_pods = [i for i in pods if i.startswith("dummy")]
    if len(dummy_pods) > 1:
        raise VALIDATIONFAIL("More than one dummy pod")
    result = dummy_pods[0]
    print(f"Our pod name: {result}")
    return result


@task(trigger=all_finished, log_stdout=True)
def print_log_output(output):
    print(output)
    # if you have many lines of logs, you may need to iterate line by line instead:
    # for line in output:
    #     print(line)


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
    del_job = delete_if_exists()
    k8s_job = create_and_run_job()
    del_job.set_downstream(k8s_job)

    pods = list_pods()
    k8s_job.set_downstream(pods)

    list_od_pods = get_pod_ids(pods)
    pod_name = get_our_pod_name(list_od_pods)
    logs = logs(pod_name)
    print_logs = print_log_output(logs)

    delete_task = delete_pod(pod_name)
    print_logs.set_downstream(delete_task)
