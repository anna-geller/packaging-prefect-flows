docker build -t daskk8 .
docker tag daskk8:latest annageller/prefect-dask-k8s:latest
docker push annageller/prefect-dask-k8s:latest
prefect register --project community -p flows/github_kubernetes_run_ephemeral_dask.py
