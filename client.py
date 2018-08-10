import socket
from sys import argv

def main():
  # Parse command line args
  if len(argv) != 3 or not argv[2].isdigit():
    print("usage: python3 client.py <server name> <server port>")
    return 1

  buffer = 2048
  name = input("Enter your name: ")


  hostname = argv[1]
  serverPort = int(argv[2])
  print("Client is running...")
  print("Remote host: {}, remote TCP port: {}".format(hostname, serverPort))

  # Create TCP socket
  clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Get IP address of server via DNS and print it(optional)
  serverIp = socket.gethostbyname(socket.gethostname())

  print("The server address is: {}:{}".format(serverIp, serverPort))

  # Connect to the server program
  clientTCP.connect((hostname, serverPort))
  print("Connected to the server")


  # send the hello message with the user’s name
  clientTCP.sendall("{} {}".format('hello', name).encode())

  while True:
    gameport = clientTCP.recv(buffer).decode().split(" ")[1]
    print("Received UDP port#:", gameport)

    # client will need to close this socket
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_address = (hostname, int(gameport))
    udpSock.connect(udp_server_address)
    break

  valid_commands = ['start', 'end', 'guess', 'exit']
  end = False  # default end flag

  # take a valid input command from a user
  message = ""
  while True:
    message = input('>>> ').lower().strip()
    if message in valid_commands or message.startswith(valid_commands[2]):
      # meaning that we need to send something to the server

      # input should contain the word guess followed by space
      if message.startswith(valid_commands[2]):
        udpSock.sendto(message.encode(), udp_server_address)
      elif valid_commands.index(message) == 0:
        udpSock.sendto("ready".encode(), udp_server_address)
      elif valid_commands.index(message) == 1:
        udpSock.sendto("end".encode(), udp_server_address)
      elif valid_commands.index(message) == 3:
        udpSock.sendto("bye".encode(), udp_server_address)


      while True:
        valid_msg_types = ["instr", "stat", "end", "na", "bye"]
        data, server = udpSock.recvfrom(4096)

        response = data.decode()


        # assume those 2 go together
        if response.startswith(valid_msg_types[0]):
          print(response)
          end = True
        if response.startswith(valid_msg_types[1]):
          chunks = response.split(" ")
          print("Word: {} Attempts left: {}".format(chunks[1], chunks[2]))
          break
        if response.startswith(valid_msg_types[2]):
          # chunks = response.split(" ")
          # print("Good luck! Word was '{}'.".format(chunks[1]))
          print(response[4:])
          break
        if response.startswith(valid_msg_types[3]):
          print(response[3:])
          break
        if response.startswith(valid_msg_types[4]):
          print("Server says bye and closes the connection")
          exit()
    else:
      print("try again")


if __name__ == "__main__":
  main()
