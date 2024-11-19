import Player from './player.js';
var socket = io();

const player = new Player('Player', Player.positions.player);
const crupier = new Player('Crupier', Player.positions.crupier);
const ai1 = new Player('AI 1', Player.positions.ai1);
const ai2 = new Player('AI 2', Player.positions.ai2);

socket.on('connect', function() {
  console.log('Connected to server');
});

// Updates the indicated player data and renders it
socket.on('update-and-render', function(data) {
  console.log('update-and-render', data);
  const player = Player.getPlayer(data.position);
  player.updateData(data);
  player.render(data.hideHand);
});


// This function is called when the start test button is clicked
// It sends a message to the server to start the test
function startTest() {
  socket.emit('start-test', { test: 'test' });
}
window.startTest = startTest;

