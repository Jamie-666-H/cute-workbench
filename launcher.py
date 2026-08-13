import os
import sys
import threading
import socketserver
import http.server

# 固定 WebView2 用户数据目录 -> 保证 localStorage 数据稳定留存（跨运行不丢）
APP_NAME = "PinkWorkbench"
appdata = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), APP_NAME)
os.makedirs(appdata, exist_ok=True)
os.environ["WEBVIEW2_USER_DATA_FOLDER"] = appdata


def resource_path(relative):
    """打包后 _MEIPASS 内为临时目录；开发时取脚本所在目录。"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


def find_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=resource_path("."), **kwargs)

    def log_message(self, *a, **k):
        pass


def start_server():
    port = find_free_port()
    httpd = socketserver.TCPServer(("127.0.0.1", port), _Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port


def main():
    import webview

    port = start_server()
    webview.create_window(
        "我的小天地 · 粉色工作台",
        url=f"http://127.0.0.1:{port}/",
        width=1180,
        height=760,
        min_size=(900, 600),
        resizable=True,
        background_color="#fff5f8",
    )
    # private_mode=False -> 允许 WebView2 持久化存储（数据本地留存）
    webview.start(private_mode=False)


if __name__ == "__main__":
    main()
