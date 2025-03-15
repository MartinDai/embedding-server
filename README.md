# embedding-server

通过代码加载embedding模型，并提供http接口服务

## 要求

python>=3.12

## 准备工作

手动下载embedding模型文件放到models目录下并命名为`embedding.gguf`，代码中使用的是[Conan-embedding-v1-Q4_K_M-GGUF](https://huggingface.co/lagoon999/Conan-embedding-v1-Q4_K_M-GGUF)，可根据实际情况替换

## 源码运行

### 安装依赖包

```shell
pip install -r requirements.txt
```

运行run.py

## 本地打包

```
make
```

打包好的可执行程序在dist目录下

**加入了gunicorn以后，单文件模式打包出来的程序执行会报错，所以使用目录模式，可以通过压缩文件夹的方式分发部署**

**如果需要更换模型，只需要替换目录_internal/models下的embedding.gguf文件即可，不需要重新打包**

## 调用接口测试
```
curl -X POST -H "Content-Type: application/json" -d '{"text":"这是一个测试句子"}' http://localhost:9999/embedding
```

## 其他

可以通过添加环境变量`LLAMA_VERBOSE=1`来打开llama_cpp的详细日志

可以通过添加环境变量`GGML_QUIET=0`来打开GGML的详细日志
