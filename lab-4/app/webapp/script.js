
// listen for keyboard input
window.addEventListener('keydown', function(event) {
  updateFrequencyElement(event.key);
  event.preventDefault();
}, true);

// frequency display
let frequency = 5
const frequencyElement = document.getElementById("freq")
frequencyElement.innerText = `${frequency} Hz`
frequencyElement.style.color = 'white'

const updateFrequencyElement = key => {
  key = key.toUpperCase()
  const canBeIncreased = key === 'A' && frequency < 10
  const canBeDecreased = key === 'D' && frequency > 1

  if (canBeIncreased) {
    frequencyElement.innerText = `${++frequency} Hz`
  } else if (canBeDecreased) {
    frequencyElement.innerText = `${--frequency} Hz`
  }
  socket.send(frequency)
}

// LED state
const ledElement = document.querySelector('main')
ledElement.style.backgroundColor = 'green'

const turnOn = () => ledElement.style.backgroundColor = 'green'
const turnOff = () => ledElement.style.backgroundColor = 'black'

// create websocket connection
const socket = new WebSocket('ws://192.168.1.210:3000')

// connection is open
socket.addEventListener('open', evt => {
    console.log('Connected to webserver!')
    socket.send(frequency)
})

// listen for incoming messages
socket.addEventListener('message', evt => {
    parseInt(evt.data) ? turnOn() : turnOff()
})

// const contrast = 8
// const darken = color => {
//   const newColor = color.slice(1).split('').map(x => {
//     x = parseInt(x, 16)
//     x = x < contrast ? 0 : x - contrast
//     return x.toString(16)
//   }).join('')
//   console.log(color, newColor)

//   return '#' + newColor
// }

// const brighten = color => {
//   return '#' + color.slice(1).split('').map(x => {
//     x = parseInt(x, 16)
//     x = x > 15 - contrast ? 15 : x + contrast
//     return x.toString(16)
//   }).join('')
// }