"""
Start the local agent with label dev:
prefect agent local start --label dev
"""
from prefect import task, Flow
from prefect.storage.local import Local
from prefect.run_configs import LocalRun


@task(log_stdout=True)
def hello_world():
    print("hello world")


with Flow(
    "local_storage_local_flow_explicit",
    storage=Local(),
    run_config=LocalRun(labels=["dev"]),
) as flow:
    hw = hello_world()

if __name__ == "__main__":
    flow.register(project_name="community")
