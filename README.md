# Working examples with various Storage and RunConfigurations

- ``flow_utilities`` shows custom utilities that may be reused across many flows.


## Building ECR image
as shown in ``commands.bash``


## Kubernetes Secrets for ``image_pull_secrets``
In order to get a custom image from a remote private container image repository, 
you need to create a Kubernetes secret object and pass it to the ``KubernetesRun`` 

Here is an example for AWS ECR:
    
    TOKEN=$(aws ecr get-login-password --region eu-central-1)
    
    kubectl create secret docker-registry aws-ecr-secret \
    --docker-server=https://123456789.dkr.ecr.eu-central-1.amazonaws.com \
    --docker-email=fake.email@example.com \
    --docker-username=AWS \
    --docker-password=$TOKEN

Note that this token is valid only for 12 hours. For production deployments, you should instead use IAM roles.

