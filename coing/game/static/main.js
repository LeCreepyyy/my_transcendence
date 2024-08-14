const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

var modal = document.getElementById("modal");

// LOGIN :

window.onclick = function() {
    modal.style.display = "none";
}

// GAME :

function getRandomIn(a, b) {
    // Crée un tableau avec les quatre nombres
    const numbers = [a, b];
    
    // Génère un index aléatoire entre 0 et 3
    const randomIndex = Math.floor(Math.random() * numbers.length);
    
    // Retourne le nombre correspondant à l'index aléatoire
    return numbers[randomIndex];
}

const paddleWidth = 10;
const paddleHeight = 100;
const ballSize = 10;

let paddle1Y = (canvas.height - paddleHeight) / 2; // Joueur 1
let paddle2Y = (canvas.height - paddleHeight) / 2; // Joueur 2
let ballX = canvas.width / 2;
let ballY = canvas.height / 2;
let ballSpeedX = getRandomIn(-5, 5);
let ballSpeedY = getRandomIn(-3, 3);
let gameInterval;
let gameRunning = false;

const paddleSpeed = 8; // Vitesse de déplacement des raquettes

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw paddles
    ctx.fillStyle = '#4CAF50'; // Couleur de la raquette
    ctx.fillRect(20, paddle1Y, paddleWidth, paddleHeight);
    ctx.fillRect(canvas.width - 20 - paddleWidth, paddle2Y, paddleWidth, paddleHeight);

    // Draw ball
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballSize, 0, Math.PI * 2);
    ctx.fillStyle = '#FF5722'; // Couleur de la balle
    ctx.fill();
}

function update() {
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    // Ball collision with top and bottom
    if (ballY <= ballSize || ballY >= canvas.height - ballSize) {
        ballSpeedY = -ballSpeedY;
    }

    // Ball collision with paddles
    if (ballX <= 30 && ballY >= paddle1Y && ballY <= paddle1Y + paddleHeight) {
        ballSpeedX = -ballSpeedX;
    }
    if (ballX >= canvas.width - 30 && ballY >= paddle2Y && ballY <= paddle2Y + paddleHeight) {
        ballSpeedX = -ballSpeedX;
    }

    // Ball out of bounds
    if (ballX < 0 || ballX > canvas.width) {
        // Reset ball
        ballX = canvas.width / 2;
        ballY = canvas.height / 2;
        ballSpeedX = -ballSpeedX;
    }

    draw();
}

function gameLoop() {
    if (gameRunning) {
        update();
        requestAnimationFrame(gameLoop); // Assure une mise à jour fluide
    }
}

function startGame() {
    if (!gameRunning) {
        gameRunning = true;
        gameLoop(); // Démarre la boucle du jeu
    }
}

function resetGame() {
    gameRunning = false;
    paddle1Y = (canvas.height - paddleHeight) / 2;
    paddle2Y = (canvas.height - paddleHeight) / 2;
    ballX = canvas.width / 2;
    ballY = canvas.height / 2;
    ballSpeedX = 5;
    ballSpeedY = 3;
    draw(); // Dessiner l'état initial
}

const keys = {}; // Objet pour stocker les touches enfoncées

document.addEventListener('keydown', (event) => {
    keys[event.key] = true; // Marquer la touche comme enfoncée
});

document.addEventListener('keyup', (event) => {
    keys[event.key] = false; // Marquer la touche comme relâchée
});

function handleControls() {
    // Contrôles du joueur 1 avec les touches W et S
    if (keys['w'] || keys['W']) {
        paddle1Y = Math.max(0, paddle1Y - paddleSpeed);
    }
    if (keys['s'] || keys['S']) {
        paddle1Y = Math.min(canvas.height - paddleHeight, paddle1Y + paddleSpeed);
    }

    // Contrôles du joueur 2 avec les touches fléchées haut et bas
    if (keys['ArrowUp']) {
        paddle2Y = Math.max(0, paddle2Y - paddleSpeed);
    }
    if (keys['ArrowDown']) {
        paddle2Y = Math.min(canvas.height - paddleHeight, paddle2Y + paddleSpeed);
    }
}

function gameLoop() {
    if (gameRunning) {
        handleControls(); // Gérer les contrôles avant la mise à jour
        update();
        requestAnimationFrame(gameLoop); // Assure une mise à jour fluide
    }
}

document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('resetButton').addEventListener('click', resetGame);
