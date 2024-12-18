export default class Player {
    static players = [];
    static positions = {
        player: 'player',
        crupier: 'crupier',
        ai1: 'ai1',
        ai2: 'ai2',
    }
    static displayStates = {
        playing: '',
        busted: 'Busted!',
        standing: 'Standing..',
        blackjack: 'Blackjack!',
    }

    /**
     * Get a player by its position
     * @param {string} position player position
     * @returns {Player}
     * @static
     */
    static getPlayer(position) {
        return Player.players.find(player => player.position === position);
    }

    constructor(name, position) {
        this.name = name;
        this.position = position;
        this.hand = [];
        this.busted = false;
        this.standing = false;
        this.state = 'playing';
        this.handValue = 0;

        Player.players.push(this);
    }

    /**
     * Render the player into its respective container
     * @param {boolean} hiddenHand if the cards should be rendered as hidden (the back)
     */
    render(hiddenHand = false) {
        this.renderPlayerBase(hiddenHand);
        if (hiddenHand) {
            this.renderHandHidden();
        } else {
            this.renderHand();
        }
    }

    /**
     * Render the player base structure.
     * This includes the player name, score and hand container
     * @param {boolean} hiddenHand if the score should be hidden
     */
    renderPlayerBase(hiddenHand = false) {
        const playerContainer = document.getElementById(this.position);
        playerContainer.innerHTML = `
            <div class="player-info">
                <div class="player-name">
                    ${this.name}
                    <span class="player-status">
                        ${Player.displayStates[this.state] || ''}
                    </span>
                </div>
                <div class="player-score">
                    ${hiddenHand ? '?' : this.handValue}
                </div>
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
     * Render the player hand 
     * This will render the cards as the back of the card
     * except for the first one
     */
    renderHandHidden() {
        const handElement = this.getPlayerElement('player-hand');
        handElement.innerHTML = '';
        this.hand.forEach((card, index) => {
            if (index === 0) {
                this.renderCard(card);
            } else {
                this.renderCard(card, true);
            }
        });
    }
        

    /**
     * Render a card into the player's hand
     * @param {Object} card card object in format `{ value, filename, color }`
     * @param {boolean} hidden if the card should be rendered as hidden (the back)
     */
    renderCard(card, hidden = false) {
        const handElement = this.getPlayerElement('player-hand');
        const cardContainer = document.createElement('div');
        cardContainer.classList.add('card-container');
        handElement.appendChild(cardContainer);
        const cardElement = document.createElement('img');
        cardElement.src = `../static/deck_scans/${hidden ? 'back_black.png' : card.filename}`;
        cardElement.classList.add('card-img');
        cardContainer.appendChild(cardElement);
    }

    renderGameResult(result) {
        const gameResults = {
            'win': 'Winner!',
            'lose': 'Loser!',
            'draw': 'Draw!',
            'busted': 'Busted!',
        }

        const playerInfo = this.getPlayerElement('player-info');
        playerInfo.innerHTML = `
            <div class="player-name">
                ${this.name}
                <span class="player-status ${result}">
                    ${gameResults[result] || ''}
                </span>
            </div>
            <div class="player-score">
                ${this.handValue}
            </div>
        `;

    }

    /**
     * Gets a element by class name from the player container
     * @param {string} className class name of the element to get
     * @returns {HTMLElement}
     */
    getPlayerElement(className) {
        return document.querySelector(`#${this.position} .${className}`);
    }

    /**
     * Update the player attributes with the data received
     * @param {Object} data data in format `{ hand, handValue, busted, standing }`
     */
    updateData(data) {
        this.hand = data.hand;
        this.handValue = data.handValue;
        this.busted = data.busted;
        this.standing = data.standing;
        this.state = data.state;
    }
}