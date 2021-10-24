# Working examples with various Storage and RunConfigurations

- ``flow_utilities`` shows custom utilities that may be reused across many flows.


## Building ECR image
as shown in ``commands.bash``


## Kubernetes Secrets for ``image_pull_secrets``
In order to get a custom image from a remote private container image repository, 
you need to create a Kubernetes secret object and pass it to the ``KubernetesRun`` 

### AWS ECR
Here is an example for AWS ECR:
    
    TOKEN=$(aws ecr get-login-password --region eu-central-1)
    
    kubectl create secret docker-registry aws-ecr-secret \
    --docker-server=https://123456789.dkr.ecr.eu-central-1.amazonaws.com \
    --docker-email=fake.email@example.com \
    --docker-username=AWS \
    --docker-password=$TOKEN

Note that this token is valid only for 12 hours. For production deployments, you should instead use IAM roles.

### Azure Container Registry

Note that ``prefectdemo`` is the registry name we've used. Change this name by your ACR name.


    ACR_NAME=prefectdemos
    SERVICE_PRINCIPAL_NAME=acr-service-principal
    
    # Obtain the full registry ID for subsequent command args
    ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query id --output tsv)
    
    # Create the service principal with rights scoped to the registry.
    # Default permissions are for docker pull access. Modify the '--role'
    # argument value as desired:
    # acrpull:     pull only
    # acrpush:     push and pull
    # owner:       push, pull, and assign roles
    SP_PASSWD=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role acrpull --query password --output tsv)
    
    kubectl create secret docker-registry aks \
    --docker-server=prefectdemos.azurecr.io \
    --docker-username=prefectdemos \
    --docker-password=$SP_PASSWD
