// For the moment we are importing the socket.io.js file from the CDN
var socket = io();

startTest = () => {
    console.log('Starting test');
    socket.emit('start-test', {
        message: 'Starting test'
    });
}

socket.on('update', (data) => {
    console.log(data);
});

socket.on('connect', () => {
    console.log('Connected to server');
});