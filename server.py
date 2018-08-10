import socket
from sys import argv
from game import *


def main():
  # Parse command line args
  if len(argv) != 2:
    print("usage: python3 server.py <word to guess or '-r' for random word>")
    return 1

  print("Server is running...")
  buffer = 2048

  # Create the TCP Socket
  print("Creating TCP socket...")
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # need to make a socket in here so we can close it
  udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  # Wait for a connection
  sock.bind(('', 0))

  # Get the port number of the socket from the OS and print it
  # print("This is my dynamically allocated port")
  print("Server is listening on the port:{}".format(sock.getsockname()[1]))

  # Configure the TCP socket (using listen) to accept a connection request

  sock.listen(10)


  try:  # try/except to catch ctrl-c
    while True:

      while True:
        conn, client_address = sock.accept()

        print("New client connected to the server")
        print(conn.recv(buffer).decode().split(' ')[1])

        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Create a UDP socket
        print("Creating UDP socket...")
        udpSock.bind(('', 0))

        updPort = udpSock.getsockname()[1];
        print("UPD socket has a port number:{}".format(updPort))

        print("Sending UDP port number to client using TCP connection...")
        # send a port to the client
        conn.send("{} {}".format("gameport", updPort).encode())
        udpSock.settimeout(120)

        active = False  # game not active by default

        # Game (UDP) loop
        while True:
          try:
            # receive on UDP port here
            data, address = udpSock.recvfrom(4096)
            print("udp ready")
            request = data.decode().split(" ")

            if request[0] == "bye":
              udpSock.sendto("{}".format("bye").encode(), address)
              # shut tcp connection
              conn.shutdown(socket.SHUT_WR)
              # close upd socket
              udpSock.close()
              active = False
              break

            elif request[0] == "ready":
             udpSock.sendto("{} {}".format("instr", INSTRUCTIONS).encode(), address)
             active = True
             game = gameSetup(argv)
             print(game)
             print("Hidden word is: {}".format(game[0]))
             print("Starting the game...")
             udpSock.sendto("{} {} {}".format("stat", game[1], game[2]).encode(), address)

            elif request[0] == "end":
              print("User gives up.")

              if not active:
                udpSock.sendto("end Nice try! But you need to start the game first".encode(), address)
              else :
                active = False
                udpSock.sendto("{} Good luck next time! The word was '{}'".format("end", game[0]).encode(), address)

            elif request[0] == "guess":
              if active and len(request) > 1:

                result = list(checkGuess(game[0], game[1], game[2], request[1], game[3]))
                result.insert(0, game[0])
                game = tuple(result)
                print(game)
                print(type(game[3]))

                # check if won the game
                if game[3]:
                  active = False
                  udpSock.sendto("{} Congratulations! You guessed the word '{}' correctly!".format("end", game[0]).encode(), address)
                elif game[2] == 0 or (game[3] == 0 and type(game[3]) == int):
                  active = False
                  udpSock.sendto("{} Good luck next time! The word was '{}'".format("end", game[0]).encode(), address)
                else:
                  udpSock.sendto("{} {} {}".format("stat", game[1], game[2]).encode(), address)

              else:
                udpSock.sendto("{} {}".format("na", "To guess the word try to start the game first").encode(), address)

               # for all other command, especially guess the active shoud be true
          except socket.timeout:  # catch UDP timeout
            print("Ending game due to timeout...")
            udpSock.close()
            break  # break and wait to accept another client

  except KeyboardInterrupt:
    # Close sockets
    print("Closing TCP and UDP sockets...")
    sock.close()
    udpSock.close()

###########################################

if __name__ == "__main__":
  main()
