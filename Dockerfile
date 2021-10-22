FROM prefecthq/prefect:0.15.6-python3.8
RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /opt/prefect
COPY flow_utilities/ /opt/prefect/flow_utilities/
COPY requirements.txt .
COPY setup.py .
RUN pip install .
COPY flows/ /opt/prefect/flows/
COPY flows_no_build/ /opt/prefect/flows/