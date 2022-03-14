import time
import mmap
import struct
import socket
import threading

def sniff(memory_map, offset=0):
    memory_map.seek(offset)
    return memory_map.read(4)

def lick(memory_map, offset=0, value=0):
    memory_map.seek(offset)
    memory_map.write(struct.pack('l', value))

def socket_sender(conn, memory_map):
    try:
        with conn:
            while True:
                conn.sendall(sniff(memory_map))
                time.sleep(0.01)  # don't DDoS the browser
    except (ConnectionResetError, BrokenPipeError):
        print('Connection dropped. Aborting sender...')
        return

def socket_listener(conn, memory_map):
    try:
        with conn:
            while True:
                data = conn.recv(12)
                if data:
                    lick(memory_map, 4, bytes2int(data))
    except (ConnectionResetError, BrokenPipeError):
        print('Connection dropped. Aborting listener...')
        return

def bytes2int(b):
    curr = 0
    for i in range(len(b)):
        curr += (b[i] - ord('0')) * 10 ** (len(b) - i - 1)
    return curr


HOST = '127.0.0.1'
PORT = 30001
BASE_ADDRESS = 0x43C00000

# open dev mem and see to base address
with open('/dev/mem', 'r+b') as f:
    with mmap.mmap(f.fileno(), 1000, offset=BASE_ADDRESS) as mem:
        # open socket server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()

            while True:
                conn, _ = s.accept()
                sender = threading.Thread(target=socket_sender, args=[conn, mem])
                listener = threading.Thread(target=socket_listener, args=[conn, mem])
                sender.start()
                listener.start()