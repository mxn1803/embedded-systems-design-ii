const { exec } = require('child_process')
const dotenv = require('dotenv').config()

const readMemory = addr => {
    return new Promise((resolve, reject) => {
        // need root password to use `/fusion2/rwmem.elf`
        const command = `echo '${process.env.PASSWD}' | sudo -S /fusion2/rwmem.elf ${addr}`
        exec(command, (err, stdout, stderr) => {
            if (err) reject(err)
            resolve(stdout.split(' = ')[1].slice(0, -1))
        })
    })
}

const writeMemory = (addr, value) => {
    return new Promise((resolve, reject) => {
        const command = `echo '${process.env.PASSWD}' | sudo -S /fusion2/rwmem.elf ${addr} ${value}`
        exec(command, (err, stdout, stderr) => {
            if (err) reject(err)
            resolve()
        })
    })
}

/**************************************************************************/

const http = require('http')
const express = require('express')
const WebSocket = require('ws')

const app = express()
const server = http.createServer(app)
const wss = new WebSocket.Server({ server })

app.use(express.static('webapp'))

// change me according to James
const READ_ADDRESS = '0x20000000'
const WRITE_ADDRESS = '0x20000000'

const hzToCounter = hz => hz * 50_000_000

wss.on('connection', ws => {
    // verify connection
    console.log('A new connection has been made.')
    ws.send('Now connected to Lab 4, Virtual LED...')

    // sniff register and send to client (100ms is about the limit for now)
    setInterval(async () => ws.send(await readMemory(READ_ADDRESS)), 100)

    // receive messages from client
    ws.on('message', async msg => {
        counter = hzToCounter(parseInt(msg))
        await writeMemory(WRITE_ADDRESS, counter)
        // console.log(counter, await readMemory(READ_ADDRESS))
    })
})

server.listen(process.env.PORT, () => {
    console.log(`Server listening on port ${process.env.PORT}!`)
})
