let timerInterval = null;

// Cronómetro
function startTimer(seconds) {
    clearInterval(timerInterval);
    let remaining = seconds;
    updateTimerDisplay(remaining);
    timerInterval = setInterval(() => {
        remaining--;
        if (remaining <= 0) {
            clearInterval(timerInterval);
            updateTimerDisplay(0);
            alert("⏰ ¡Tiempo de descanso completado! A por la siguiente serie.");
        } else {
            updateTimerDisplay(remaining);
        }
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
    updateTimerDisplay(0);
}

function updateTimerDisplay(sec) {
    const m = String(Math.floor(sec / 60)).padStart(2, '0');
    const s = String(sec % 60).padStart(2, '0');
    document.getElementById("timerDisplay").innerText = `${m}:${s}`;
}
