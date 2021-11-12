import prefect
from prefect import Flow, task
from prefect.run_configs import VertexRun
from prefect.storage import GitHub


FLOW_NAME = "github_vertexrun"
STORAGE = GitHub(
    repo="anna-geller/packaging-prefect-flows",
    path=f"flows/{FLOW_NAME}.py",
    access_token_secret="GITHUB_ACCESS_TOKEN",  # required with private repositories
)
RUN_CONFIG = VertexRun()


@task(log_stdout=True)
def hello_world():
    text = f"hello from {FLOW_NAME} from Prefect version {prefect.__version__}"
    print(text)
    return text


with Flow(FLOW_NAME, run_config=RUN_CONFIG,) as flow:
    hw = hello_world()
