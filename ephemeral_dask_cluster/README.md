# Ephemeral Dask Cluster on Kubernetes

Example using:
- a custom public Docker image pushed to Dockerhub so that all Dask workers and K8s agent can access it
- GitHub storage to store flow code

Note that this public image has no custom package dependencies. 
To include those, ideally build a custom image and push it to a registry of your choice e.g. AWS ECR, 
and set up permissions on the Kubernetes cluster using IAM roles. 

As a workaround, you can leverage Kubernetes registry secrets, as described in the main README of the repo, 
but then you need to ensure that all Dask workers can also pull this image, otherwise you'll get ``ErrImagePull``.
This would need to be somehow configured in dask.yml in the ``Role``. 