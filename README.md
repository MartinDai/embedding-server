# embedding-server

通过代码加载embedding模型，并提供http接口服务

## 要求

python>=3.12

## 准备工作

手动下载embedding模型文件放到models目录下，代码中使用的是[Conan-embedding-v1-Q4_K_M-GGUF](https://huggingface.co/lagoon999/Conan-embedding-v1-Q4_K_M-GGUF)，可根据实际情况替换

## 源码运行

### 安装依赖包

```shell
pip install -r requirements.txt
```

运行app.py

## 本地打包

```
make
```

打包好的可执行程序在dist目录下

## 调用接口测试
```
curl -X POST -H "Content-Type: application/json" -d '{"text":"这是一个测试句子"}' http://localhost:9999/embedding
```