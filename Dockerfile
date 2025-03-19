FROM rockylinux:8.9 AS builder

WORKDIR /tmp

RUN dnf update -y
RUN dnf install -y python3.12 python3.12-devel
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip wheel

RUN dnf install -y gcc gcc-c++ make git
RUN dnf install -y openblas

RUN pip3 install PyInstaller==6.12.0
RUN pip3 install --no-binary numpy numpy==2.2.4

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# 复制源代码并构建二进制
COPY . .
RUN python3 -m PyInstaller --strip --noupx \
    --add-data 'models/:models/' \
    --add-data '.env:.' \
    --hidden-import gunicorn \
    --collect-all gunicorn \
    --hidden-import llama_cpp \
    --add-binary '/usr/local/lib64/python3.12/site-packages/llama_cpp:llama_cpp' \
    run.py -n embedding-server

FROM rockylinux:8.9

WORKDIR /app/embedding-server
# 从 builder 阶段复制构建好的二进制文件
COPY --from=builder /app/dist/embedding-server ./

# 设置默认命令
CMD ["/app/embedding-server/embedding-server"]