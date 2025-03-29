# embedding-server

通过代码加载embedding模型，并提供http接口服务

## 要求

python>=3.12

## 准备工作

下载onnx格式的模型文件夹放到models目录下并命名为`onnx`

## 本地运行

### 安装依赖包

```shell
pip install pdm
pdm install
```

运行run.py

## 本地打包镜像

```
make
```

## 指定架构打包镜像

```shell
make linux-amd64
```

## 调用接口测试
```
curl -X POST -H "Content-Type: application/json" -d '{"text":"这是一个测试句子"}' http://localhost:8080/embedding
```

## 环境变量

可以在`.env`文件添加修改支持的环境变量