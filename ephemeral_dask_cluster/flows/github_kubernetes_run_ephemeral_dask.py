"""
Example from https://medium.com/slateco-blog/prefect-x-kubernetes-x-ephemeral-dask-power-without-responsibility-6e10b4f2fe40
"""
from dask_kubernetes import KubeCluster, make_pod_spec
import prefect
from prefect import task, Flow
from prefect.executors import DaskExecutor
from prefect.run_configs import KubernetesRun
from prefect.storage import GitHub

# Configure a storage object, by default prefect's latest image will be used
FLOW_NAME = "github_kubernetes_run_ephemeral_dask"
STORAGE = GitHub(
    repo="anna-geller/packaging-prefect-flows",
    path=f"ephemeral_dask_cluster/flows/{FLOW_NAME}.py",
    access_token_secret="GITHUB_ACCESS_TOKEN",  # required with private repositories
)


@task
def extract() -> list:
    return [1, 2, 3, 4, 5, 6]


@task
def transform(number: int) -> int:
    return number * 2


@task()
def load(numbers: list) -> list:
    return [i for i in numbers if i]


with Flow(
    FLOW_NAME,
    storage=STORAGE,
    executor=DaskExecutor(
        cluster_class=lambda: KubeCluster(make_pod_spec(image=prefect.context.image)),
        adapt_kwargs={"minimum": 2, "maximum": 3},
    ),
    run_config=KubernetesRun(
        labels=["dask"],
        image="annageller/prefect-dask-k8s:latest",
    ),
) as flow:
    nrs = extract()
    tranformed_numbers = transform.map(nrs)
    numbers_twice = transform.map(tranformed_numbers)
    result = load(numbers=numbers_twice)
