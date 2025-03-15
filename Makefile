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

.PHONY: pre build

pre:
	pip install -r requirements.txt
	pip install pyinstaller

build: $(TARGET)

linux-amd64:
	docker buildx build --platform linux/amd64 -t embedding-amd64-builder -o type=docker .
	docker run --platform linux/amd64 --rm -v `pwd`:/app -w /app embedding-amd64-builder /bin/bash -c "python3 -m PyInstaller --strip --noupx --name app_linux-amd64 --add-data '/app/models:models' --add-binary '/usr/local/lib64/python3.12/site-packages/llama_cpp:llama_cpp' --onefile app.py"
linux-arm64:
	docker buildx build --platform linux/arm64 -t embedding-arm64-builder -o type=docker .
	docker run --platform linux/arm64 --rm -v `pwd`:/app -w /app embedding-arm64-builder /bin/bash -c "python3 -m PyInstaller --strip --noupx --name app_linux-arm64 --add-data '/app/models:models' --add-binary '/usr/local/lib64/python3.12/site-packages/llama_cpp:llama_cpp' --onefile app.py"

darwin-arm64: pre
	pyinstaller --name app_darwin-arm64 --add-data "models:models" --add-binary ".venv/lib/python3.12/site-packages/llama_cpp:llama_cpp" --onefile app.py
