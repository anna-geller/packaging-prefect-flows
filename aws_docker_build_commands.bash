docker build -t community .
# to check the files in the container
docker run --rm -it community
aws ecr create-repository --repository-name community --image-scanning-configuration scanOnPush=true

docker tag community:latest 338306982838.dkr.ecr.us-east-1.amazonaws.com/community:latest
aws ecr get-login-password | docker login --username AWS --password-stdin 338306982838.dkr.ecr.us-east-1.amazonaws.com
docker push 338306982838.dkr.ecr.us-east-1.amazonaws.com/community:latest
