import Player from './player.js';
var socket = io();

const player = new Player('Player', Player.positions.player);
const crupier = new Player('Crupier', Player.positions.crupier);
const ai1 = new Player('AI 1', Player.positions.ai1);
const ai2 = new Player('AI 2', Player.positions.ai2);

socket.on('connect', function() {
  console.log('Connected to server');
});

socket.on('update-and-render', function(data) {
  console.log('update-and-render', data);
  const player = Player.getPlayer(data.position);
  player.updateData(data);
  player.render();
});


function startTest() {
  socket.emit('start-test', { test: 'test' });
}
window.startTest = startTest;
// we are using modules, so we need to export the function to the window object



// let testCards = [
//   { value: 2, fileName: '2_of_clubs.png', color: 'black' },
//   { value: 3, fileName: '3_of_clubs.png', color: 'black' },
//   { value: 4, fileName: '4_of_clubs.png', color: 'red' },
//   { value: 5, fileName: '5_of_clubs.png', color: 'black' },
//   { value: 11, fileName: 'ace_of_clubs.png', color: 'black' }
// ];
// player.hand = testCards;
// player.handValue = 24;
// player.render();
// crupier.hand = testCards;
// crupier.render(true);
// ai1.render();
// ai2.render();

// setTimeout(() => {
//   player.hand.push({ value: 3, fileName: '3_of_clubs.png', color: 'black' });
//   player.render();
// }, 2000);
