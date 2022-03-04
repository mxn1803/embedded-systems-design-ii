let count = 5;
update(count);

// listen for keyboard input
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
    count = Math.round(evt.data)
    update(evt.data)
})


// Change Frequency w keys
function change_freq(key){
  if (key == 'a') {
    if (count == 0) {count = 0;}
    else {count--;}
  }
  else if (key =='d'){
    if (count == 10){count = 10;}
    else {count++;}
  }
  update(count);
  socket.send(count);
}

// Update frequency heading display
function update(frequency){
  document.getElementById("freq").innerHTML = frequency + " Hz";
  color(frequency);
}


// Update Page (LED) color
function color(frequency){
  background=document.querySelector("main")
  if (frequency == 0){
    background.style.backgroundColor = 'black';
    document.getElementById("freq").style.color = 'white';


    //Is there a way to actually dim screen or did you just mean turn it black?
  }
  else {
    background.style.backgroundColor = "#60F360";
    document.getElementById("freq").style.color = 'black';
  }
}