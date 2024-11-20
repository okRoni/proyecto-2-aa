import Player from './player.js';
var socket = io();

// Entities
const player = new Player('Player', Player.positions.player);
const crupier = new Player('Crupier', Player.positions.crupier);
const ai1 = new Player('AI 1', Player.positions.ai1);
const ai2 = new Player('AI 2', Player.positions.ai2);
const players = [player, ai1, ai2];

// Elements
const startButton = document.getElementById('start');
const hitButton = document.getElementById('hit');
hitButton.disabled = true;
const standButton = document.getElementById('stand');
standButton.disabled = true;
const hitSafeText = document.getElementById('hit-safe-prob');
// hitSafeText.hidden = true;
const reportsButton = document.getElementById('reports-button');

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

socket.on('start-player-turn', function(data) {
  hitButton.disabled = false;
  standButton.disabled = false;
});

socket.on('end-player-turn', function(data) {
  hitButton.disabled = true;
  standButton.disabled = true;
});

socket.on('game-over', function(data) {
  startButton.disabled = false;
  reportsButton.disabled = false;
  for (const player of players) {
    player.renderGameResult(data[player.position]);
  }
});

// This function is called when the start test button is clicked
// It sends a message to the server to start the test
function startTest() {
  socket.emit('start-test', { test: 'test' });
  startButton.disabled = true;
  reportsButton.disabled = true;
}
window.startTest = startTest;

function handleHitAction() {
  socket.emit('player-move', { move: 'hit' });
}
window.handleHitAction = handleHitAction;

function handleStandAction() {
  socket.emit('player-move', { move: 'stand' });}

window.handleStandAction = handleStandAction;

