FROM python:3.13-slim

WORKDIR /app

ARG INSTALL_HEAVY=1

# Always install small runtime deps
RUN pip install --no-cache-dir \
    requests \
    pika

# Optionally install heavy ML libs if requested at build time
RUN if [ "${INSTALL_HEAVY}" = "1" ] ; then \
      pip install --no-cache-dir "transformers>=4.57.3,<5.0.0" "torch>=2.9.1,<3.0.0" ; \
    else \
      echo "Skipping heavy ML libs (set INSTALL_HEAVY=1 to install)" ; \
    fi

COPY . .

CMD ["python", "consumer.py"]
