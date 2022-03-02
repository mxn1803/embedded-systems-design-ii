const http = require('http')
const net = require('net')
const express = require('express')
const WebSocket = require('ws')
const dotenv = require('dotenv').config()

const app = express()
const server = http.createServer(app)
const wss = new WebSocket.Server({ server })
const snifferConnection = net.createConnection({
    host: '127.0.0.1',
    port: 30001
})

app.use(express.static('webapp'))

const hzToCounter = hz => hz * 50_000_000
const dataBufferToCounter = buf => {
    return (buf[3] << 24) + (buf[2] << 16) + (buf[1] << 8) + buf[0]
}

wss.on('connection', ws => {
    // verify connection
    console.log('A new connection has been made.')
    ws.send('Now connected to Lab 4, Virtual LED...')

    snifferConnection.on('data', data => {
        // chunk into single readings
        chunk = Buffer.alloc(4)
        for (const [idx, byte] of data.entries()) {
            chunk[idx % 4] = byte
            if (idx % 4 === 3) {
                value = dataBufferToCounter(chunk)
                ws.send(value)
                chunk.fill(0)
            }
        }
    })

    ws.on('message', data => {
        data = hzToCounter(parseInt(data.toString()))

        // write me to memory
        console.log(data)
    })
})

server.listen(process.env.PORT, () => {
    console.log(`Server listening on port ${process.env.PORT}!`)
})
