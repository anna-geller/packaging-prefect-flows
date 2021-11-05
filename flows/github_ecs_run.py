import prefect
from prefect import Flow, task
from prefect.storage import GitHub
from prefect.run_configs import ECSRun


FLOW_NAME = "github_ecs_run"
STORAGE = GitHub(
    repo="anna-geller/packaging-prefect-flows",
    path=f"flows/{FLOW_NAME}.py",
    access_token_secret="GITHUB_ACCESS_TOKEN",  # required with private repositories
)
RUN_CONFIG = ECSRun(
    labels=["prod"],
    run_task_kwargs=dict(cluster="prefectEcsCluster", launchType="FARGATE",),
)


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    return text


with Flow(
    FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,
) as flow:
    hw = hello_world()
