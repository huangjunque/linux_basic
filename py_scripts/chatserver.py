#!/usr/bin/env python
#coding=utf-8
from asyncode import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 8888
NAME = ‘TESTCHAT’
class EndSession(Exception):
    pass

class CommandHandler:
    """
    类似于标准库重的cmd.Cmd的简单命令处理程序
    """

    def unkown(self, session, cmd):
        '响应未知命令'
        session.push('unkown command: %s\r\n' % cmd)

    def handler(self, session, line):
        if not line.strip):
            return
        parts = line.split(' ', 1)

        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        #试着查找处理程序:
        meth = getattr(self, 'do_'+cmd, None)
        try:
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)

class Room(CommandHandler):
    """
    包括一个或多个用户的(会话)的泛型环境,它负责基本的命令处理和广播.
    """

    def __init__(self, server):
        self.server = server
        self.session = []

    def add(self, session):
        '一个会话（用户）已进入房间'
        self.session.append(session)

    def remove(self, session):
        '一个会话(用户) 已离开房间'
        self.session.remove(session)

    def broadcast(self, line):
        '向房间中所有会话发送一行'
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        '响应logout命令'
        raise EndSession

class LoginRoom(Room):
    """
     为刚刚连接上的用户准备的房间.
    """
