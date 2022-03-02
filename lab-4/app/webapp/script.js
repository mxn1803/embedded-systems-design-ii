let count = 5;
update(count);

window.addEventListener('keydown', function(event) {
    change_freq(event.key);
    event.preventDefault();
}, true);



// create websocket connection
const socket = new WebSocket('ws://localhost:3000')

// connection is open
socket.addEventListener('open', evt => {
    console.log('Connected to webserver!')
})

// listen for incoming messages
socket.addEventListener('message', evt => {
    console.log(`Server: ${evt.data}`)
})


// Change Frequency w keys
function change_freq(name){
  if (name == 'a') {
    if (count == 0) {count = 0;}
    else {count--;}
    update(count);
    socket.send(count)
  }
  else if (name =='d'){
    if (count == 10){count = 10;}
    else {count++;}
    update(count);
    socket.send(count)
  }
}

// Update display
function update(frequency){
  document.getElementById("freq").innerHTML = frequency + " Hz";
  color(frequency);
}


//Update Page (LED) color
function color(frequency){
  background=document.querySelector("main")
  if (frequency == 0){
    background.style.backgroundColor = 'black';
    document.getElementById("freq").style.color = 'white';
  }
  else {
    background.style.backgroundColor = "green";
    document.getElementById("freq").style.color = 'black';
  }
}

//set up web socket connection
//read/write freq
// change to freq to be fpga readable