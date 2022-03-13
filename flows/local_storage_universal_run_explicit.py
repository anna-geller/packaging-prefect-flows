"""
Start the local agent with label dev:
prefect agent local start --label dev
"""
from prefect import task, Flow
from prefect.storage.local import Local
from prefect.run_configs import UniversalRun


@task(log_stdout=True)
def hello_world():
    print("hello world")


with Flow(
    "local_storage_universal_run_explicit",
    storage=Local(),
    run_config=UniversalRun(
        labels=["xxx"], env={"PREFECT__CLOUD__SEND_FLOW_RUN_LOGS": False}
    ),
) as flow:
    hw = hello_world()
