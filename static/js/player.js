export default class Player {
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

    constructor(name, position) {
        this.name = name;
        this.position = position;
        this.hand = [];
        this.busted = false;
        this.standing = false;
        this.hideHand = false;
    }

    /**
     * Render the player into its respective container
     */
    render() {
        this.renderPlayerBase();
        this.renderHand();
    }

    /**
     * Render the player base structure.
     * This includes the player name, score and hand container
     */
    renderPlayerBase() {
        const playerContainer = document.getElementById(this.position);
        playerContainer.innerHTML = `
            <div class="player-info">
                <div class="player-name">${this.name}</div>
                <div class="player-score">0</div>
            </div>
            <div class="player-hand"></div>
        `;
    }

    /**
     * Render the player hand
     * This will render the cards in the player's hand
     */
    renderHand() {
        const handElement = this.getPlayerElement('player-hand');
        handElement.innerHTML = '';
        this.hand.forEach(card => {
            this.renderCard(card);
        });
    }

    /**
     * Render a card into the player's hand
     * @param {Object} card card object in format `{ value, fileName, color }`
     */
    renderCard(card) {
        const handElement = this.getPlayerElement('player-hand');
        const cardContainer = document.createElement('div');
        cardContainer.classList.add('card-container');
        handElement.appendChild(cardContainer);
        const cardElement = document.createElement('img');
        cardElement.src = `../static/deck_scans/${card.fileName}`;
        cardElement.classList.add('card-img');
        handElement.appendChild(cardElement);
    }

    /**
     * Gets a element by class name from the player container
     * @param {string} className class name of the element to get
     * @returns {HTMLElement}
     */
    getPlayerElement(className) {
        return document.querySelector(`#${this.position} .${className}`);
    }
}