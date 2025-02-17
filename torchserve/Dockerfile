FROM pytorch/torchserve:latest

COPY torchserve/model-store /home/model-server/model-store
COPY torchserve/requirements.txt /home/model-server/requirements.txt
WORKDIR /home/model-server/

RUN pip install --no-cache-dir -r requirements.txt

# CMD ["torchserve", "--start", "--model-store", "model-store", "--models", "sismedbert=sismedbert.mar"]
