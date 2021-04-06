var socketio = io.connect('http://localhost:8080');

const form = document.getElementById('form');
var username = undefined;
var roomcode = undefined;
const container = document.getElementById('message-container');


// When you have room code
form.onsubmit = (e) => {

    e.preventDefault();
    var user = document.getElementById("username").value;
    var room = document.getElementById("roomcode").value;
    if(user === "" || room === "")return;
    console.log(user,room);

    // Send the room code to server for authentication
    socketio.emit('check-room',{
        username:user,
        room_id:room
    });

    // check if room code is valid
    socketio.on('if-room',json => {
        console.log(json['user'],"special "+room);
        if(json['user']==user){
            if(json['present']){
                socketio.emit('join',{
                    username:user,
                    roomcode:room
                });
                appendPreviousMessages(json['message_list']);
                username = user;
                roomcode = room;
                document.getElementById("login-form").classList.add("hide-class");
                document.getElementById("message-section").classList.remove("hide-class");
                document.getElementById("greetings").innerHTML = `Welcome ${user} to chat room ${room}!!`;
            }else{
                alert('There is no room with this id');
                document.getElementById("username").value = "";
                document.getElementById("roomcode").value = "";
                console.log('not in list');
            }
        }
    });
}

// Append previous messages
const appendPreviousMessages = (messages) => {
    container.innerHTML = "";
    for(let i=0;i<messages.length;i++){
        var div = document.createElement('div');
        div.innerHTML = `<strong> ${messages[i].user} </strong>: ${messages[i].message}`;
        container.appendChild(div);
    }
    //console.log(messages);
}

// Collect message and pass to server
var message_form = document.getElementById('message-form');
message_form.onsubmit = e => {
    e.preventDefault();
    const message = document.getElementById('message').value;
    document.getElementById('message').value = "";
    document.getElementById('message').focus();
    console.log(message);
    socketio.emit('message-pass',{
        user_name:username,
        message:message,
        room:roomcode
    });
}


// Recieve message from server
socketio.on('display-client',(data) => {
    if(container.innerHTML == 'No Messages yet..')
        container.innerHTML = "";
    if(roomcode == undefined){
        roomcode = data.roomcode;
        document.getElementById("greetings").innerHTML = `Welcome ${username} to chat room ${roomcode}!!`;
    }
    var div = document.createElement('div');
    div.innerHTML = `<strong> ${data.user_name} </strong>: ${data.message}`;
    container.appendChild(div);
});


// When you generate new room
document.getElementById('create-room').onclick = () => {
    var username_input = document.getElementById("username")
    if(username_input.value.length != 0){
        // generate a new code request to the server
        socketio.emit('join',{
            username:username_input.value,
        });

        //add new roomid after a room is created by someone 
        socketio.on('add-new-roomcode',(data) => {
            roomcode = data['room']
        });

        username = username_input.value;
        document.getElementById("greetings").innerHTML = `Welcome ${username} to chat room ${roomcode}!!`;
        document.getElementById("login-form").classList.add("hide-class");
        document.getElementById("message-section").classList.remove("hide-class");
    }
};

// Leave Room Button
document.getElementById('leave-room').onclick = () => {
    console.log('Leaving room');
    socketio.emit('leave',{
        username:username,
        room:roomcode
    });

    window.location.reload();

    document.getElementById("login-form").classList.remove("hide-class");
    document.getElementById("message-section").classList.add("hide-class");
    container.innerHTML = "No Messages yet..";
    username = "";
    roomcode = "";   
}
