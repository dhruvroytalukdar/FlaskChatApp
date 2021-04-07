var socketio = io.connect('http://localhost:8080');

const form = document.getElementById('form');
var username = undefined;
var roomcode = undefined;
const container = document.getElementById('message-container');
const member_count_id = document.getElementById("member_count_id");

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
                username = user;
                roomcode = room;

                // Add previous messages into the client
                appendPreviousMessages(json['message_list']);
                
                // set number of members in the room currently 
                member_count_id.innerHTML = json['members'].toString();
                
                document.getElementById("login-form").classList.add("hide-class");
                document.getElementById("message-section").classList.remove("hide-class");
                document.getElementById("greetings").innerHTML = `Welcome ${user} to chat room ${room}!!`;
            }else{
                alert(json['error']);
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
        console.log(messages[i].user);
        if(username != messages[i].user){   
            var div = document.createElement('div');
            div.innerHTML = `<strong> ${messages[i].user} </strong>: ${messages[i].message}`;
        }else{
            var div = document.createElement('div');
            div.innerHTML = `${messages[i].message} :<strong> ${messages[i].user} </strong>`;
            div.classList.add('mymessages');
        }
        div.onclick = handleDeleteFunction;
        container.appendChild(div);
    }
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
    
    // Check if the data has members properties
    if(data.hasOwnProperty('members')){
        member_count_id.innerHTML = data['members'].toString();
    }

    if(username != data.user_name){   
        var div = document.createElement('div');
        div.innerHTML = `<strong> ${data.user_name} </strong>: ${data.message}`;
    }else{
        var div = document.createElement('div');
        div.innerHTML = `${data.message} :<strong> ${data.user_name} </strong>`;
        div.classList.add('mymessages');
    }
    div.setAttribute("id",data.id.toString());
    div.onclick = handleDeleteFunction;
    container.appendChild(div);
});

// When you want to delete a message
const handleDeleteFunction = (e) => {
    var parentdiv;
    if(e.srcElement.parentNode == container)
        parentdiv = e.srcElement;
    else
        parentdiv = e.srcElement.parentNode;
    console.log(parentdiv);
    if(parentdiv.classList.contains("mymessages") && parentdiv.getAttribute("id") !== "temp"){
        if(confirm("Do you really want to delete your message?")){
            socketio.emit("delete-message",{
                id:parentdiv.getAttribute("id"),
                room:roomcode
            })
        }
    }
}

// Remove message from he html page
socketio.on("remove-message",json => {
    var div = document.getElementById(json["id"])
    container.removeChild(div);
})


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
