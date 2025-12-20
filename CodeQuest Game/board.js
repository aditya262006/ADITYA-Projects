const board = document.getElementById('board');
const gridIndex = (r,c) => r*5 + c;
const pathOrder = [];
for(let r=0;r<5;r++){
  if(r%2===0){ for(let c=0;c<5;c++) pathOrder.push([r,c]); }
  else { for(let c=4;c>=0;c--) pathOrder.push([r,c]); }
}
const starIndices = [2,4,7,10,11,13,15,18,22,24];
const qIndices = [5,9,14,17,20,23];
const cells = [];
for(let i=0;i<25;i++){
  const div = document.createElement('div');
  div.className = 'cell fill'; div.dataset.index = i;
  board.appendChild(div); cells.push(div);
}
for(let i=0;i<pathOrder.length;i++){
  const [r,c] = pathOrder[i]; const idx = gridIndex(r,c); const el = cells[idx];
  el.classList.remove('fill'); el.classList.add('path');
  if(i===0){ const b=document.createElement('div'); b.className='badge start'; b.textContent='START'; el.appendChild(b); }
  else if(i===pathOrder.length-1){ const b=document.createElement('div'); b.className='badge end'; b.textContent='END'; el.appendChild(b); }
  if(starIndices.includes(i+1)){ el.classList.add('star-glow'); const m=document.createElement('div'); m.className='marker star'; m.textContent='★'; el.appendChild(m); }
  if(qIndices.includes(i+1)){ el.classList.add('q-glow'); const m=document.createElement('div'); m.className='marker q'; m.textContent='?'; el.appendChild(m); }
  const prev = (i>0)? pathOrder[i-1] : null; const next = (i<pathOrder.length-1)? pathOrder[i+1] : null;
  const r0=r, c0=c;
  function isUp(a){ return a && a[0]===r0-1 && a[1]===c0; } function isDown(a){ return a && a[0]===r0+1 && a[1]===c0; }
  function isLeft(a){ return a && a[0]===r0 && a[1]===c0-1; } function isRight(a){ return a && a[0]===r0 && a[1]===c0+1; }
  if(isUp(prev) || isUp(next)) el.classList.add('conn-up'); if(isDown(prev) || isDown(next)) el.classList.add('conn-down');
  if(isLeft(prev) || isLeft(next)) el.classList.add('conn-left'); if(isRight(prev) || isRight(next)) el.classList.add('conn-right');
  const dbg = document.createElement('div'); dbg.style.cssText='position:absolute; right:6px; bottom:6px; font-size:11px; color:rgba(255,255,255,0.9)';
  dbg.textContent = i+1; el.appendChild(dbg);
}

document.getElementById('helpIcon').onclick = () => {
  window.open('help/help.html', '_blank', 'width=900,height=600');
};

  if (!sessionStorage.getItem("fromLoader")) {
    window.location.replace("loadingscreen.html");
  } else {
    sessionStorage.removeItem("fromLoader");
  }

// ===================================
//  SCRIPT 2: GAME INTERACTION LOGIC
// ===================================
const pawn = document.getElementById('pawn');
const cube = document.getElementById('cube');
const rollBtn = document.getElementById('rollBtn');
const resultCard = document.getElementById('resultCard');
const gameStats = {
  playerName: "",
  startTime: Date.now(),
  puzzlesPlayed: {},
  totalScore: 0
};
function registerPuzzleResult(name, success) {
  const p = gameStats.puzzlesPlayed[name];
  if (!p) return;
  const timeTaken = Math.floor((Date.now() - p.start) / 1000);
  let score = 0;
  if (success) {
    if (timeTaken <= 20) score = 150;
    else if (timeTaken <= 40) score = 120;
    else if (timeTaken <= 60) score = 100;
    else if (timeTaken <= 90) score = 70;
    else score = 40;
  }
  p.success = success;
  p.time = timeTaken;
  p.score = score;
  gameStats.totalScore += score;
}
// Game State
let currentPawnIndex = 0;
let isInteracting = false;
let mustSolvePuzzle = false;
let activePuzzleTile = null;
// --- Pawn Functions ---
function placePawnAt(pathIndex) {
  const [row, col] = pathOrder[pathIndex];
  const cellWidth = board.clientWidth / 5;
  const cellHeight = board.clientHeight / 5;
  pawn.style.width = `${cellWidth * 0.45}px`;
  pawn.style.height = `${cellHeight * 0.65}px`;
  const pawnX = col * cellWidth + (cellWidth / 2);
  const pawnY = row * cellHeight + (cellHeight / 2);
  pawn.style.left = `${pawnX}px`;
  pawn.style.top = `${pawnY}px`;
}
function handleEvent(tileNumber) {
    const challengeMap = {
        2: { name: 'Code Unlock', file: 'codeunlock.html' },
        4: { name: 'Wordle', file: 'wordle.html' },
        7: { name: 'Logic Detective', file: 'logicdetective.html' },
        9: { name: 'Sudoku Timer Puzzle', file: 'sudoku.html' },
        10: { name: 'Hangman', file: 'hangman.html' },
        11: { name: 'Tech Riddle', file: 'techriddle.html' },
        13: { name: 'Crack the Logic', file: 'crackthelogic.html' },
        14: { name: 'Word Finder', file: 'wordfinder2.html' },
        15: { name: 'Sudoku', file: 'sudokuu.html' },
        18: { name: 'Guess the Number', file: 'guessthenumber.html' },
        22: { name: 'Memory Hacker', file: 'memoryhacker.html' },
        23: { name: 'Hangman Puzzle', file: 'hangman2.html' },
        24: { name: 'Word Finder', file: 'wordfinder.html' }
    };
    if (challengeMap[tileNumber]) {
        const challenge = challengeMap[tileNumber];
        alert(`You've landed on the ${challenge.name} challenge! ★`);
        openPuzzle(challenge, tileNumber);
        return;
    } else if (starIndices.includes(tileNumber)) {
        alert(`Landed on challenge tile ${tileNumber}. No game here yet!`);
        rollBtn.disabled = false;
        isInteracting = false;
    } else if (qIndices.includes(tileNumber)) {
        switch (tileNumber) {
            case 5:
                setTimeout(() => {
                    alert("You found a shortcut! Move 3 steps ahead.");
                    movePawn(3);
                }, 200);
                break;
            case 17:
                setTimeout(() => {
                    alert("You fell into a trap! Move 3 steps backward.");
                    movePawn(-3);
                }, 200);
                break;
            case 20:
                setTimeout(() => {
                    alert("A vortex sends you back to the start!");
                    const stepsBack = -currentPawnIndex;
                    movePawn(stepsBack);
                }, 200);
                break;
            default:
                rollBtn.disabled = false;
                isInteracting = false;
        }
    } else {
        rollBtn.disabled = false;
        isInteracting = false;
    }
}
function getGrade(score) {
  if (score >= 1400) return "S";
  if (score >= 1100) return "A";
  if (score >= 800) return "B";
  if (score >= 500) return "C";
  return "D";
}
function gameWon() {
  startConfetti(8000);
  const totalTime = Math.floor((Date.now() - gameStats.startTime) / 1000);
  const grade = getGrade(gameStats.totalScore);
  document.getElementById("playerSummary").innerHTML = `
    ⏱ Total Time: <b>${totalTime}s</b><br>
    🧠 Puzzles Cleared: <b>${Object.keys(gameStats.puzzlesPlayed).length}</b><br>
    ⭐ Total Score: <b>${gameStats.totalScore}</b><br>
    🏅 Rank: <span style="font-size:1.6rem;color:gold"><b>${grade}</b></span>
  `;
  document.getElementById("winModal").classList.remove("hidden");
}
function downloadShareCard() {
  const name = prompt("Enter your name:");
  if (!name) return;
  const grade = getGrade(gameStats.totalScore);
  const c = document.getElementById("shareCanvas");
  const ctx = c.getContext("2d");
  // Background
  const grad = ctx.createLinearGradient(0,0,0,c.height);
  grad.addColorStop(0, "#020617");
  grad.addColorStop(1, "#0f172a");
  ctx.fillStyle = grad;
  ctx.fillRect(0,0,c.width,c.height);
  // Glow
  ctx.shadowColor = "gold";
  ctx.shadowBlur = 40;
  // Title
  ctx.fillStyle = "#facc15";
  ctx.font = "bold 72px Cinzel Decorative";
  ctx.textAlign = "center";
  ctx.fillText("ADVENTURE QUEST", c.width/2, 150);
  ctx.shadowBlur = 0;
  // Player Info
  ctx.fillStyle = "#f8fafc";
  ctx.font = "48px Inter";
  ctx.fillText(`Player: ${name}`, c.width/2, 280);
  // Score
  ctx.font = "44px Inter";
  ctx.fillText(`Score: ${gameStats.totalScore}`, c.width/2, 360);
  // Rank Badge
  ctx.fillStyle = "gold";
  ctx.beginPath();
  ctx.arc(c.width/2, 480, 90, 0, Math.PI*2);
  ctx.fill();
  ctx.fillStyle = "#020617";
  ctx.font = "bold 96px Inter";
  ctx.fillText(grade, c.width/2, 515);
  // Puzzle Breakdown
  let y = 650;
  ctx.textAlign = "left";
  ctx.font = "36px Inter";
  for (let p in gameStats.puzzlesPlayed) {
    const g = gameStats.puzzlesPlayed[p];
    const icon = g.success ? "✔" : "✖";
    ctx.fillStyle = g.success ? "#22c55e" : "#ef4444";
    ctx.fillText(`${icon} ${p}  (${g.time}s)  +${g.score}`, 140, y);
    y += 55;
  }
  // Download
  const link = document.createElement("a");
  link.download = `${name}_AdventureQuest_${grade}.png`;
  link.href = c.toDataURL("image/png");
  link.click();
}
function openPuzzle(challenge, tileNumber) {
  mustSolvePuzzle = true;
  activePuzzleTile = tileNumber;
  rollBtn.disabled = true;
  if (!gameStats.puzzlesPlayed[challenge.name]) {
    gameStats.puzzlesPlayed[challenge.name] = {
      start: Date.now(),
      success: false,
      score: 0
    };
  }
  document.getElementById('puzzleTitle').textContent = challenge.name;
  document.getElementById('puzzleFrame').src = challenge.file;
  document.getElementById('puzzleOverlay').classList.remove('hidden');
}

function gameLost() {
  document.getElementById("loseModal").classList.remove("hidden");
}
function resetPlayerToStart() {
  currentPawnIndex = 0;
  placePawnAt(0);
  gameLost(); // 🔥 THIS OPENS THE LOSE MODAL
}
function completePuzzle(success = true) {
  if (!mustSolvePuzzle) return;
  const puzzleName = document.getElementById('puzzleTitle').textContent;
  mustSolvePuzzle = false;
  activePuzzleTile = null;
  document.getElementById('puzzleFrame').src = '';
  document.getElementById('puzzleOverlay').classList.add('hidden');
  isInteracting = false;
  if (success) {
    // ✅ RECORD SUCCESS + SCORE
    registerPuzzleResult(puzzleName, true);
    rollBtn.disabled = false;
  } else {
    // ❌ RECORD FAILURE
    registerPuzzleResult(puzzleName, false);
    rollBtn.disabled = true;
    setTimeout(() => {
      resetPlayerToStart();
      rollBtn.disabled = false;
    }, 400);
  }
}
function startConfetti(duration = 5000) {
  const canvas = document.getElementById("confettiCanvas");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const pieces = Array.from({ length: 250 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height - canvas.height,
    size: Math.random() * 6 + 4,
    speed: Math.random() * 4 + 2,
    color: `hsl(${Math.random() * 360},100%,60%)`
  }));
  let start = performance.now();
  function draw(time) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pieces.forEach(p => {
      p.y += p.speed;
      if (p.y > canvas.height) p.y = -20;
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x, p.y, p.size, p.size);
    });
    if (time - start < duration) requestAnimationFrame(draw);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  requestAnimationFrame(draw);
}
function movePawn(steps) {
  isInteracting = true;
  const totalTiles = pathOrder.length;
  const targetIndex = Math.min(totalTiles - 1, Math.max(0, currentPawnIndex + steps));
  if (targetIndex === currentPawnIndex) {
    isInteracting = false;
    rollBtn.disabled = false;
    return;
  }
  const direction = targetIndex > currentPawnIndex ? 1 : -1;
  const interval = setInterval(() => {
    if (currentPawnIndex !== targetIndex) {
      currentPawnIndex += direction;
      placePawnAt(currentPawnIndex);
    } else {
      clearInterval(interval);
      const currentTileNumber = currentPawnIndex + 1;
      if (currentPawnIndex === totalTiles - 1) {
        setTimeout(() => {
          gameWon();
          startConfetti(8000);
          rollBtn.disabled = true;
        }, 100);
      } else {
        setTimeout(() => handleEvent(currentTileNumber), 100);
      }
    }
  }, 400);
}
// --- Dice Functions ---
const faceRotations = {
  1: { x: 0, y: 0 }, 6: { x: 0, y: 180 }, 2: { x: 0, y: -90 },
  5: { x: 0, y: 90 }, 3: { x: -90, y: 0 }, 4: { x: 90, y: 0 }
};
function rollDice() {
  if (isInteracting) return;
  isInteracting = true;
  rollBtn.disabled = true;
  resultCard.textContent = 'Rolling...';
  const result = Math.floor(Math.random() * 6) + 1;
  const spinsX = Math.floor(Math.random() * 2) + 1;
  const spinsY = Math.floor(Math.random() * 2) + 1;
  const base = faceRotations[result];
  const finalX = base.x + spinsX * 360;
  const finalY = base.y + spinsY * 360;
  cube.style.transform = `rotateX(${finalX}deg) rotateY(${finalY}deg)`;
  cube.addEventListener('transitionend', () => {
    resultCard.innerHTML = `You rolled a <strong>${result}</strong>!`;
    movePawn(result);
  }, { once: true });
}

// --- INITIALIZATION ---
window.addEventListener('load', () => {
    const savedIndex = sessionStorage.getItem('boardGamePawnIndex');
    if (savedIndex !== null) {
        currentPawnIndex = parseInt(savedIndex, 10);
        sessionStorage.removeItem('boardGamePawnIndex');
    }
    setTimeout(() => {
        placePawnAt(currentPawnIndex);
    }, 100);
    rollBtn.addEventListener('click', rollDice);
});
// Frontend Chatbot Logic
document.addEventListener('DOMContentLoaded', () => {
    const openChatBtn = document.getElementById('open-chat-btn');
    const closeChatBtn = document.getElementById('close-chat-btn');
    const chatbotModal = document.getElementById('chatbot-modal');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatLog = document.getElementById('chat-log');

    openChatBtn.addEventListener('click', () => {
        chatbotModal.classList.remove('hidden');
    });

    closeChatBtn.addEventListener('click', () => {
        chatbotModal.classList.add('hidden');
    });

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight; 
    }

    async function sendMessage() {
        const question = chatInput.value.trim();
        if (!question) return;
        addMessage(question, 'user');
        chatInput.value = '';
        try {
            const response = await fetch('http://localhost:3000/ask-chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            const data = await response.json();
            addMessage(data.answer, 'bot');
        } catch (error) {
            console.error('Error fetching chatbot response:', error);
            addMessage('Sorry, I am having trouble connecting. Please try again later.', 'bot');
        }
    }
});

(function () {
  const modal = document.getElementById("chatbot-modal");
  const header = document.getElementById("chat-header");

  let isDragging = false, offsetX = 0, offsetY = 0;

  header.style.cursor = "move";

  header.addEventListener("mousedown", e => {
    isDragging = true;
    offsetX = e.clientX - modal.offsetLeft;
    offsetY = e.clientY - modal.offsetTop;
  });

  document.addEventListener("mousemove", e => {
    if (!isDragging) return;
    modal.style.left = e.clientX - offsetX + "px";
    modal.style.top = e.clientY - offsetY + "px";
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });
})();