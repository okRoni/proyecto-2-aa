class Player {
    static players = [];
    static positions = {
        player: 'player',
        crupier: 'crupier',
        ai1: 'ai1',
        ai2: 'ai2',
    }

    static getPlayer(position) {
        return Player.players.find(player => player.position === position);
    }

    constructor(position) {
        this.position = position;
        this.hand = [];
        this.busted = false;
        this.standing = false;
        this.hideHand = false;
    }

    render() {
        this.renderPlayer();
        this.renderHand();
    }

    renderPlayer() {
        const playerContainer = document.createElement('div');
        const player = 
        player.classList.add('player');
        player.id = this.position;
        player.innerHTML = `
            <div class="player-info">
                <div class="player-name">${this.position}</div>
                <div class="player-score">0</div>
            </div>
            <div class="player-hand"></div>
        `;
    }

    renderHand() {
    }
}