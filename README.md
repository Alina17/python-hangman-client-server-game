# python-hangman-client-server-game
Python Client/Server "Hangman" game using TCP/UDP


Simple game of Hangman using client /server, implementing both TCP and UDP connections. Language: Python 3.6.5 
Coded on Windows machine using JetBrains PyCharm community edition 2018, tested via subversion Bash on Ubuntu on Windows 
Server-side program accepts single command line –r which will pick word randomly.  
Client program should accept two parameters that allow user to specify the server ip address and port number. Note: server will choose random open port, which will be used on client side.  
The client program asks for the name of the user, then waits for "start" to start the game. After this command, user will see instructions for the game, hidden words number of letters, which represented as "-", and number of attempts to guess. In order to start guessing, use the command "guess" space "character". If you know which word is hidden, can enter "guess" space "word". If guessed letter if wrong, number of attempts will decrease and shows on the screen. If word is not guessed correct, you can start guessing new word by typing "start" again. If you give up and want to guess the word, enter "end", which will show the word, and you can enter "start" again to guess the word. If you enter "exit" it will close closes TCP connection and exits UDP. Screen shoots are provided to show the game in action.
