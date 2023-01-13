#! /usr/bin/python
# encoding:utf-8

import socket, select
import uuid

# server ip、port
sever_host = '0.0.0.0'
sever_port = 8080

file_total_size = 594
# file path
file_path = "/opt/file/"
file_name = str(uuid.uuid4())
received_size = 0


def main():
    global received_size,file_name
    CONNECTION_LIST = []  # list of socket clients
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((sever_host, sever_port))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print("Chat server started on port " + str(sever_port))

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:

            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    received_size += len(data)
                    mode = "wb"
                    f = open(file_path + file_name, mode)
                    if data.endswith('end'):
                        print('data received end')
                        data = data[0:-3]
                        f.write(data)
                        received_size = 0
                        f.close()
                        file_name = str(uuid.uuid4())
                        break
                    if received_size > 0:
                        f.write(data)

                # client disconnected, so remove from socket list
                except Exception as N:
                    print(N)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()


if __name__ == "__main__":
    main()
