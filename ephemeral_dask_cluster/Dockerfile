FROM prefecthq/prefect:0.15.6-python3.8
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install dask-kubernetes==2021.10.0
WORKDIR /opt/prefect
COPY flows/ /opt/prefect/flows/
# RUN apt-get update && apt-get install -y curl &&\
#     curl -LO https://dl.k8s.io/release/v1.21.2/bin/linux/amd64/kubectl &&\
#     install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl &&\
#     rm -rf /var/lib/apt/lists/*