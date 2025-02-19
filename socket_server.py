import socket
import socketserver
import threading
import logging

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            if isinstance(self.request, socket.socket):  # 确保是套接字对象
                data = self.request.recv(1024)
                if data:
                    print(f"收到数据: {data.decode()}")
                    self.request.sendall(data)
                else:
                    print("客户端断开连接")
            else:
                print("错误：self.request 不是套接字对象")
        except socket.error as e:
            print(f"套接字操作失败: {e}")
        finally:
            if isinstance(self.request, socket.socket):
                self.request.close()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

    def server_close(self):
        print("关闭服务器套接字")
        super().server_close()

def run_server():
    HOST, PORT = "localhost", 5000
    try:
        with ReusableTCPServer((HOST, PORT), MyTCPHandler) as server:
            print(f"服务器已启动，监听 {HOST}:{PORT}")
            server.serve_forever()
    except OSError as e:
        print(f"服务器启动失败: {e}")
    except KeyboardInterrupt:
        print("服务器正在关闭...")
    finally:
        print("服务器已关闭")

if __name__ == '__main__':
    run_server() 