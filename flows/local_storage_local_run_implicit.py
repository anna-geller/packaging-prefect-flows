"""
Since those are defaults, we don't necessarily have to specify anything, only start the local agent:
prefect agent local start
"""
from prefect import task, Flow


@task(log_stdout=True)
def hello_world():
    print("hello world")


with Flow("local_storage_local_run_implicit") as flow:
    hw = hello_world()

if __name__ == "__main__":
    flow.register(project_name="community")
