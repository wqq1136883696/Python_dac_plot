import socket
import time


class StpCaComm(object):
    """"""
    def __init__(self, ip='localhost', port=1001):
        """初始化，构造函数"""
        self.ip = ip
        self.port = port
        self.socket = None

        # 连接条纹相机程序
        try:
            self.socket = socket.create_connection((ip, port), timeout=10)
        except Exception as err:
            print("StpCaComm:Connection error - {}".format(err))
            # raise err

    def __send(self, message):
        # StrCaComm - Send a message to the Stripe Camera
        # 发送消息给条纹相机

        total_sent = 0

        # # Prepend the message length to the message.
        # message = str(len(message)).zfill(2) + message

        # Send the message， 发送消息
        while total_sent < len(message):
            try:
                sent = self.socket.send((message[total_sent:] + "\r").encode())
            except Exception as err:
                print("StrCaComm:Send communication error - {}".format(err))
                sent = 0
                # raise err

            # If sent is zero, there is a communication issue
            if sent == 0:
                raise RuntimeError("StrCaComm:Cryostation connection lost on send")
            total_sent = total_sent + sent

    def __receive(self):
        # StrCaComm - Receive a message from the StrCaComm
        # 接收返回的消息
        chunks = []
        received = 0

        # Read the message
        try:
            chunk = self.socket.recv(4096)
        except Exception as err:
            print("StrCaComm:Receive communication error - {}".format(err))
            chunk = 0
            # raise err

        # If an empty chunk is read, there is a communication issue
        if chunk == b'':
            raise RuntimeError("StrCaComm:Stripe Camera connection lost on receive")

        chunks.append(chunk)
        received += len(chunk)

        return ''.join([x.decode('UTF8') for x in chunks])

    def __receive_loop(self):
        # StrCaComm - Receive a message from the StrCaComm
        # 接收返回的消息
        chunks = []
        received = 0

        try:
            self.socket.settimeout(6000)
            chunk = self.socket.recv(1024)
        except Exception as err:
            print("StrCaComm:Receive communication error - {}".format(err))
            # raise err
            chunk = b"0"

        # If an empty chunk is read, there is a communication issue
        if chunk == '':
            pass
            # raise RuntimeError("StrCaComm:Stripe Camera connection lost on receive")
        chunks.append(chunk)
        received += len(chunk)
        return ''.join([x.decode('UTF8') for x in chunks])

    def send_command_get_response(self, message):
        # StrCaComm - Send a message to the Stripe Camera and receive a response

        self.__send(message)
        # return self.__receive()
        return "ok"

    def receive(self):
        # 接收消息
        return self.__receive()

    def receive_message(self):
        # StrCaComm - 接收消息
        return self.__receive_loop()

    def close(self):
        return self.__del__()

    def __del__(self):
        # StrCaComm - Destructor,摧毁连接

        if self.socket:
            self.socket.shutdown(1)
            self.socket.close()
