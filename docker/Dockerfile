FROM python:3.10-slim

ARG USER_ID
ARG USER_NAME
ARG LLM_MODEL_NAME

ENV HOME=/home/${USER_NAME} \
    VIRTUAL_ENV=/home/${USER_NAME}/venv

ENV \
  PYTHONUNBUFFERED=1 \
  DEBIAN_FRONTEND=noninteractive  \
  PYTHONPATH="/app:${PYTHONPATH}" \
  BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

RUN apt-get -qq update \
    && apt-get -qq -y install vim gcc curl git build-essential libb64-dev software-properties-common \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

RUN addgroup --system --gid ${USER_ID} ${USER_NAME} \
    && useradd --system -m --no-log-init --home-dir ${HOME} --uid ${USER_ID} --gid ${USER_NAME} --groups ${USER_NAME} ${USER_NAME} \
    && chown -R ${USER_NAME}:${USER_NAME} ${HOME}

RUN mkdir -p /app && chown -R ${USER_NAME}:${USER_NAME} /app /tmp

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/home/${USER_NAME}/.local/bin:${PATH}"

COPY pyproject.toml *.lock /app/

WORKDIR /app

# Change ownership of .local directory
RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}/.local

RUN poetry config virtualenvs.create false \
    && python3.10 -m venv ${VIRTUAL_ENV} \
    && pip install --upgrade pip setuptools \
    && poetry install && cp poetry.lock ${BUILD_POETRY_LOCK} \
    && rm -rf ${HOME}/.cache/*

# Install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the model file to the container
COPY docker/modelfile /app/

# Switch to the non-root user
USER ${USER_NAME}

# Create the model using ollama
RUN ollama create ${LLM_MODEL_NAME} -f /app/modelfile



#RUN ollama create ${LLM_MODEL_NAME} -f /app/modelfile

USER root
COPY ./docker/scripts/* /
RUN chown -R ${USER_NAME} /*.sh && chmod +x /*.sh
USER ${USER_NAME}

COPY . /app/

# Run uvicorn when the container launches
#CMD ["uvicorn", "app.code_gen.main:app", "--host", "0.0.0.0", "--port", "8000"]
