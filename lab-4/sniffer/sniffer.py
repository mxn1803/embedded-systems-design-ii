import os
import socket
import time

HOST = '127.0.0.1'
PORT = 30001
READ_ADDRESS = 0xFF

def sniff(mem_address):
    # open memory file
    fd = os.open('/dev/mem', os.O_RDONLY | os.O_SYNC)

    # open socket server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            try:
                connection, _ = s.accept()
                with connection:
                    for i in range(0xFFFF):
                        value = os.pread(fd, 4, mem_address)
                        connection.sendall(value)
                        time.sleep(0.01)
            except ConnectionResetError:
                print('Connection reset by peer.')
            except BrokenPipeError:
                print('Broken pipe.')

    os.close(fd)

sniff(READ_ADDRESS)