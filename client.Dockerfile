##############################################################################
##                                 Base Image                               ##
##############################################################################
ARG PYTHON_VERSION=3.10.12
FROM python:$PYTHON_VERSION AS base
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LANG=C.UTF-8
ENV LC_ALL=C

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    bash nano htop git sudo wget curl gedit pip && \
    rm -rf /var/lib/apt/lists/*

##############################################################################
##                                 User                                     ##
##############################################################################
FROM base AS user

# Create user
ARG USER=robot
ENV USER=$USER
ARG PASSWORD=automaton
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID $USER \
    && useradd -m -u $UID -g $GID -p "$(openssl passwd -1 $PASSWORD)" \
    --shell $(which bash) $USER -G sudo

USER $USER

##############################################################################
##                            Dependencies                                 ##
##############################################################################
FROM user AS dependencies

# RUN pip install --upgrade pip build
RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir fastapi uvicorn msgpack
RUN pip install --no-cache-dir requests
RUN pip install hydra-core --upgrade
ENV PATH="/home/$USER/.local/bin:${PATH}"

RUN mkdir -p /home/$USER/workspace
COPY --chown=$USER:$USER ./clip_nerf/src/configs /home/$USER/workspace/configs
WORKDIR /home/$USER/workspace
CMD ["python3", "src/main.py"]
