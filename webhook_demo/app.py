"""
这是一个演示 xray webhook 功能的 Python app，请勿在生产环境直接使用
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

debug = True
# FIXME thread lock
statistics = None
plugin_vuln_count = {}


def process_vuln(data):
    plugin = data["plugin"]
    if plugin not in plugin_vuln_count:
        plugin_vuln_count[plugin] = 1
    else:
        plugin_vuln_count[plugin] += 1
    # 在这里拿到漏洞数据之后还可以干很多事情，比如自行存入数据库、微信推送、钉钉推送等，相关文档可以参考
    # http://sc.ftqq.com/3.version
    # https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq


def process_statistics(data):
    global statistics
    statistics = data


# 访问首页就可以看到统计数据
@app.route("/", methods=["GET"])
def index():
    # FIXME 使用 token 来保证 api 安全
    return jsonify({"statistics": statistics, "plugin_vuln_count": plugin_vuln_count})


@app.route("/webhook", methods=["POST"])
def xray_webhook():
    # FIXME 使用 token 来保证 api 安全
    data = request.json
    # 目前是通过这个字段来区分统计数据和漏洞数据的，之后将在 http header 中加入字段区分
    if "vuln_class" in data:
        process_vuln(data)
    else:
        process_statistics(data)
    return "ok"


if __name__ == "__main__":
    app.run(debug=debug)
