docker build -t flow_utilities .
# to check the files in the container
docker run --rm -it flow_utilities

# make sure to create ACR registry for your flows (e.g. in Azure UI)
az acr login --name prefectcommunity
docker tag flow_utilities:latest prefectcommunity.azurecr.io/images/flow_utilities:latest
docker push prefectcommunity.azurecr.io/images/flow_utilities:latest
