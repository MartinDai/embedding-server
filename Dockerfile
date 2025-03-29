FROM python:3.12-slim

WORKDIR /app/embedding-server

# 复制依赖文件并安装
COPY pyproject.toml pdm.lock ./
RUN pip install pdm && pdm install --no-editable -v

# 复制源代码和配置文件
COPY . .

# 设置默认命令
ENTRYPOINT ["pdm", "run", "gunicorn"]
CMD ["-b", "0.0.0.0:8080", "run:app"]