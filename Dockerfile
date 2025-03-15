FROM rockylinux:8.9

WORKDIR /tmp

RUN dnf update -y
RUN dnf install -y python3.12 python3.12-devel
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip wheel

RUN dnf install -y gcc gcc-c++ make git
RUN dnf install -y openblas

RUN pip3 install PyInstaller==6.12.0

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-binary numpy numpy==2.2.3 && \
    pip3 install -r requirements.txt

CMD ["/bin/bash"]