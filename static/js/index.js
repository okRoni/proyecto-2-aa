import Player from './player.js';

// For the moment we are importing the socket.io.js file from the CDN
var socket = io();


const player = new Player('Player', Player.positions.player);
let testCards = [
  { value: 2, fileName: '2_of_clubs.png', color: 'black' },
  { value: 3, fileName: '3_of_clubs.png', color: 'black' },
  { value: 4, fileName: '4_of_clubs.png', color: 'red' },
  { value: 11, fileName: 'ace_of_clubs.png', color: 'black' }
];
player.hand = testCards;
player.render();


