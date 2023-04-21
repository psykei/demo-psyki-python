FROM python:3.9
EXPOSE 8888
RUN apt update; apt install -y -q openjdk-17-jdk
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /root/.jupyter
ENV JUPYTER_CONF_FILE /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.allow_origin = '*'" > $JUPYTER_CONF_FILE
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> $JUPYTER_CONF_FILE
RUN mkdir -p /notebooks
COPY */*.ipynb /notebooks/
COPY data /notebooks/data
COPY knowledge /notebooks/knowledge
COPY utils /notebooks/utils
WORKDIR /notebooks
CMD jupyter notebook --allow-root --no-browser