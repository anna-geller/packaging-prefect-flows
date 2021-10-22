"""
Start the local agent with label dev:
prefect agent local start --label dev
"""
from prefect import task, Flow
from prefect.storage.local import Local
from prefect.run_configs import LocalRun

# as long as those custom modules are installed on the local agent with label "dev"
# and on the machine from which you register the flow, this will work
from flow_utilities.db import get_df_from_sql_query


@task(log_stdout=True)
def hello_world():
    print("hello world")


with Flow(
    "local_storage_local_run_explicit_custom_modules",
    storage=Local(),
    run_config=LocalRun(labels=["dev"]),
) as flow:
    hw = hello_world()
