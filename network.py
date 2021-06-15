import socket
import pickle
import struct
import traceback


class Network(object):
    def __init__(self, ip, port, password):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.p = self.connect(password)

    def getP(self):
        return self.p

    def connect(self, password = 'pirosulti'):
        try:
            print(" [*] in network.connect")
            self.client.connect(self.addr)
            print("connect done")
            self.client.send(password.encode())
            print("before getting auth response")
            result = self.client.recv(4096).decode()
            print("getting auth result from server: ", result)
            if result == 'authenticated':
                print('authenticated')
                return self.client.recv(4096).decode()
            else:
                print("not authenticated")
                self.client.close()
        except:
            pass

    def send(self, data, sent_data_id):
        try:
            # self.client.send(str.encode(data))
            # return pickle.loads(self.client.recv(4096*64))
            # send data
            serialized_payload = pickle.dumps(data)
            # print(" [*] network send length struct:", struct.pack('>I', len(serialized_payload)))
            self.client.sendall(struct.pack('>I', len(serialized_payload)))
            # print(" [*] network send id struct:", sent_data_id)
            self.client.sendall(struct.pack('>I', sent_data_id))
            # print(" [*] network payload: ", serialized_payload)
            self.client.sendall(serialized_payload)
            # receive game object
            recv_data_size = struct.unpack('>I', self.client.recv(4))[0]
            # print("recv data size", recv_data_size)
            recv_data_id = struct.unpack('>I', self.client.recv(4))[0]
            # print("recv data id", recv_data_id)
            recv_payload = b""
            remaining_payload_size = recv_data_size
            while remaining_payload_size != 0:
                recv_payload += self.client.recv(remaining_payload_size)
                remaining_payload_size = recv_data_size - len(recv_payload)
            # print("recv payload: ", recv_payload)
            result = pickle.loads(recv_payload)
            # print("result type:", type(result))
            # print("result:", result)
            return result



        except socket.error as e:
            print(e)

    def send_player_object(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096*64))
        except socket.error as e:
            print(e)


server = "192.168.178.24"
port = 5555
