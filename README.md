# Fask Real Time ChatApp

## Features

* Provides realtime features of a basic chat app
* Rooms can be created and specific members can be added based on the creators choice
* Rooms will display name and number of members online
* If you left the chat room and at least one member is still online then all the chats will persist in case of rejoin
* One can delete their own message and that message will be deleted for all the room members

## APIs Used

* MySQL Database for storing Chats and Chat Rooms
* Flask as a server
* Flask-SocketIO for server side socketio implementation
* SocketIO.js for client side socketio implementation
* Plain HTML,CSS and Vanila Javascript for UI design and client side rendering **(can be upgraded to Vue.js in the future)**