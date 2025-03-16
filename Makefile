# 获取系统信息
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)

# 检测系统架构并选择对应目标
ifeq ($(UNAME_S),Linux)
    ifeq ($(UNAME_M),x86_64)
        TARGET = linux-amd64
    else ifeq ($(UNAME_M),aarch64)
        TARGET = linux-arm64
    else
        $(error Unsupported architecture: $(UNAME_M))
    endif
else ifeq ($(UNAME_S),Darwin)
    ifeq ($(UNAME_M),arm64)
        TARGET = darwin-arm64
    else
        $(error Unsupported architecture for macOS: $(UNAME_M))
    endif
else
    $(error Unsupported OS: $(UNAME_S))
endif

# 默认执行目标
.DEFAULT_GOAL := build

.PHONY: pre build linux-amd64 linux-arm64 darwin-arm64

# 预安装依赖
pre:
	pip install -r requirements.txt
	pip install pyinstaller

# 通用的 PyInstaller 参数
PYINSTALLER_BASE_OPTS = --strip --noupx \
	--add-data 'models/embedding.gguf:models/' \
	--hidden-import gunicorn \
	--collect-all gunicorn \
	--hidden-import llama_cpp

# 构建规则
build: $(TARGET)

linux-amd64:
	rm -rf dist/embedding-server-linux-amd64
	docker buildx build --platform linux/amd64 -t embedding-amd64-builder -o type=docker .
	docker run --platform linux/amd64 --rm \
		-v "$$(pwd)":/app -w /app embedding-amd64-builder \
		/bin/bash -c "python3 -m PyInstaller $(PYINSTALLER_BASE_OPTS) --add-binary '/usr/local/lib64/python3.12/site-packages/llama_cpp:llama_cpp' run.py -n embedding-server-linux-amd64"

linux-arm64:
	rm -rf dist/embedding-server-linux-arm64
	docker buildx build --platform linux/arm64 -t embedding-arm64-builder -o type=docker .
	docker run --platform linux/arm64 --rm \
		-v "$$(pwd)":/app -w /app embedding-arm64-builder \
		/bin/bash -c "python3 -m PyInstaller $(PYINSTALLER_BASE_OPTS) --add-binary '/usr/local/lib64/python3.12/site-packages/llama_cpp:llama_cpp' run.py -n embedding-server-linux-arm64"

darwin-arm64: pre
	rm -rf dist/embedding-server-darwin-arm64
	python3 -m PyInstaller $(PYINSTALLER_BASE_OPTS) \
		--add-binary '.venv/lib/python3.12/site-packages/llama_cpp:llama_cpp' \
		run.py -n embedding-server-darwin-arm64