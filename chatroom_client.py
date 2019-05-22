'''
    客户端
'''

from socket import *
import os, sys

ADDR = ("127.0.0.1", 8888)


# 创建网络连接
def main():
    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)

    while True:
        # 等待客户端输入信息
        name = input("Enter name:")
        msg = "L " + name  # L后加空格为了方便解析

        # 向服务端发送信息
        s.sendto(msg.encode(), ADDR)

        # 接收服务端反馈信息并决定接下来的操作
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    # 创建新进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


# 发送消息
def send_msg(s, name):
    while True:
        try:
            text = input("Say:")
        except KeyboardInterrupt:
            text = "quit"
        # 退出聊天室
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")

        # 参与聊天
        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(1024)
        # 服务端发送exit表示让客户端退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode())


if __name__ == "__main__":
    main()
