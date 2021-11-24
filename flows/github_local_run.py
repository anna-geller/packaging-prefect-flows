from prefect import Flow, task
from prefect.storage import GitHub
from prefect.run_configs import LocalRun


FLOW_NAME = "github_local_run"
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
    FLOW_NAME, storage=STORAGE, run_config=LocalRun(labels=["dev"],),
) as flow:
    hw = hello_world()
