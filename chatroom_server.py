'''
    服务器端
'''

from socket import *
import os, sys

ADDR = ("0.0.0.0", 8888)
# 用于存储用户信息
user = {}


# 创建网络连接
def main():
    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定地址
    s.bind(ADDR)

    # 请求处理
    do_request(s)  # 处理客户端请求

    # 关闭套接字
    s.close()


# 接收各种客户端请求
def do_request(s):
    while True:
        # 收发消息
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(" ")

        # 区分请求类型
        if msg[0] == "L":
            do_login(s, msg[1], addr)
        elif msg[0] == "C":
            do_chat(s, msg[1], " ".join(msg[2:]))
        elif msg[0] == "Q":
            do_quit(s, msg[1])
        else:
            pass


# 处理客户端的登录请求
def do_login(s, name, addr):
    if name in user:
        s.sendto("该用户已存在".encode(), addr)
        return
    s.sendto(b"OK", addr)

    # 循环通知其他人
    msg = "欢迎%s加入聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])

    # 将该用户加入
    user[name] = addr


# 处理客户端的聊天请求
def do_chat(s, name, text):
    msg = "%s : %s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


# 处理客户端的退出请求
def do_quit(s, name):
    for i in user:
        if i != name:
            s.sendto("%s已退出群聊" % name, user[i])
        else:
            s.sendto(b"EXIT", user[i])
    del user[name]


if __name__ == "__main__":
    main()
