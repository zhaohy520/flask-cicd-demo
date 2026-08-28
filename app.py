# Flask 演示应用（CI/CD 流水线的被测对象）
# 两个接口：
#   GET /        -> 首页（显示版本号和主机名，用于演示自动更新）
#   GET /healthz -> 健康检查（k8s 探针专用，永远返回 200）
import os
import socket

from flask import Flask

app = Flask(__name__)

# 版本号来自构建参数/环境变量（CI 流水线会注入 commit SHA）
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route("/")
def hello():
    hostname = socket.gethostname()
    return (
        f"<h1>Hello CI/CD! 🚀</h1>"
        f"<p>version: <b>{VERSION}</b></p>"
        f"<p>hostname: {hostname}</p>"
    )


@app.route("/healthz")
def healthz():
    # k8s 的 liveness/readiness 探针打这里（不重定向、稳定 200）
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
