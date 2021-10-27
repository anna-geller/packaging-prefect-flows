kubectl apply -f dask.yml # make sure to adjust your agent labels and API key in dask.yml
docker build -t daskk8 .
docker tag daskk8:latest annageller/prefect-dask-k8s:latest
docker push annageller/prefect-dask-k8s:latest
prefect create project community
prefect register --project community -p flows/github_kubernetes_run_ephemeral_dask.py
