"""
Plantilla HTML5 moderna, responsiva y con modo oscuro para el Dashboard Interactivo de GymFit Agent.
Permite interactuar visualmente con el núcleo funcional, simular cronómetros y probar eventos de variabilidad.
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GymFit Agent — Dashboard Interactivo</title>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --bg-input: #334155;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border: #334155;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            padding: 12px;
            line-height: 1.5;
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: transparent;
        }

        @media (min-width: 768px) {
            body {
                padding: 20px;
            }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header */
        header {
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: var(--bg-secondary);
            padding: 14px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 16px;
        }

        @media (min-width: 768px) {
            header {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                padding: 16px 24px;
                margin-bottom: 24px;
            }
        }

        .header-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            gap: 12px;
        }

        .header-title h2 {
            font-size: 1.25rem;
        }

        @media (min-width: 768px) {
            .header-title {
                width: auto;
                justify-content: flex-start;
            }
            .header-title h2 {
                font-size: 1.5rem;
            }
        }

        .header-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            width: 100%;
        }

        .header-actions .btn {
            font-size: 0.8rem;
            padding: 9px 8px;
            justify-content: center;
            text-align: center;
        }

        .header-actions a.btn {
            grid-column: span 2;
        }

        @media (min-width: 768px) {
            .header-actions {
                display: flex;
                width: auto;
                gap: 10px;
            }
            .header-actions .btn {
                font-size: 0.88rem;
                padding: 10px 16px;
            }
            .header-actions a.btn {
                grid-column: auto;
            }
        }

        .badge {
            background: rgba(34, 197, 94, 0.15);
            color: var(--success);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid rgba(34, 197, 94, 0.3);
            white-space: nowrap;
        }

        /* Pastilla del split activo: permite salto de línea en pantallas angostas */
        #routineSplitBadge {
            white-space: normal;
            word-break: break-word;
            overflow-wrap: break-word;
            max-width: 100%;
            text-align: center;
            line-height: 1.4;
            border-radius: 8px;
            flex-shrink: 1;
        }

        .btn {
            background: var(--accent);
            color: #0f172a;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            touch-action: manipulation;
        }

        .btn:hover {
            background: var(--accent-hover);
            color: #ffffff;
        }

        .btn-secondary {
            background: var(--bg-input);
            color: var(--text-primary);
        }

        .btn-secondary:hover {
            background: #475569;
        }

        .btn-danger {
            background: rgba(239, 68, 68, 0.2);
            color: var(--danger);
            border: 1px solid var(--danger);
        }

        .btn-danger:hover {
            background: var(--danger);
            color: white;
        }

        .btn-warning {
            background: rgba(245, 158, 11, 0.2);
            color: var(--warning);
            border: 1px solid var(--warning);
        }

        .btn-warning:hover {
            background: var(--warning);
            color: white;
        }

        /* Grid */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }

        @media (min-width: 900px) {
            .grid-2 {
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 24px;
            }
        }

        /* Cards */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px;
        }

        @media (min-width: 768px) {
            .card {
                padding: 20px;
            }
        }

        .card-header {
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }

        .card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        @media (min-width: 768px) {
            .card-title {
                font-size: 1.15rem;
            }
        }

        /* Forms */
        .form-group {
            margin-bottom: 12px;
        }

        .form-row-2 {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }

        @media (min-width: 480px) {
            .form-row-2 {
                grid-template-columns: 1fr 1fr;
            }
        }

        .form-row-3 {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }

        @media (min-width: 440px) {
            .form-row-3 {
                grid-template-columns: 1fr 1fr 1fr;
            }
        }

        label {
            display: block;
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-bottom: 5px;
            font-weight: 500;
        }

        input, select {
            width: 100%;
            padding: 10px 12px;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 16px; /* Evita zoom automático en Safari iOS */
        }

        input:focus, select:focus {
            outline: 2px solid var(--accent);
        }

        /* Equipment Chips */
        .chips-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 8px;
        }

        .chip {
            background: var(--bg-input);
            padding: 7px 12px;
            border-radius: 9999px;
            font-size: 0.82rem;
            cursor: pointer;
            user-select: none;
            border: 1px solid var(--border);
            transition: all 0.2s;
            touch-action: manipulation;
        }

        .chip.selected {
            background: rgba(56, 189, 248, 0.2);
            color: var(--accent);
            border-color: var(--accent);
            font-weight: 600;
        }

        /* Explanation Box */
        .agent-bubble {
            background: rgba(56, 189, 248, 0.08);
            border-left: 4px solid var(--accent);
            padding: 12px 14px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 16px;
            font-size: 0.9rem;
            color: #e0f2fe;
            line-height: 1.5;
        }

        @media (min-width: 768px) {
            .agent-bubble {
                padding: 14px 18px;
                font-size: 0.95rem;
                margin-bottom: 20px;
            }
        }

        /* Routine View */
        .day-card {
            background: #182234;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 14px;
        }

        @media (min-width: 768px) {
            .day-card {
                padding: 14px;
            }
        }

        .day-header {
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            justify-content: space-between;
            align-items: center;
            font-size: 0.95rem;
        }

        @media (min-width: 768px) {
            .day-header {
                font-size: 1rem;
            }
        }

        .exercise-item {
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .exercise-item:first-child {
            padding-top: 2px;
        }

        .exercise-item:last-child {
            border-bottom: none;
            padding-bottom: 2px;
        }

        .exercise-name {
            font-size: 0.95rem;
            font-weight: 600;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 4px 8px;
            margin-bottom: 6px;
        }

        @media (min-width: 768px) {
            .exercise-name {
                font-size: 1rem;
            }
        }

        .exercise-line {
            font-size: 0.82rem;
            color: #94a3b8;
            margin-top: 4px;
            line-height: 1.45;
            word-break: break-word;
        }

        .exercise-line strong {
            color: #f1f5f9;
            font-weight: 600;
        }

        /* Timer Box */
        .timer-box {
            text-align: center;
            padding: 16px 10px;
            background: #111827;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-top: 14px;
        }

        @media (min-width: 768px) {
            .timer-box {
                padding: 20px;
            }
        }

        .timer-display {
            font-size: 2.3rem;
            font-weight: 800;
            font-family: monospace;
            color: var(--accent);
            margin: 6px 0;
            letter-spacing: 0.05em;
        }

        @media (min-width: 600px) {
            .timer-display {
                font-size: 2.8rem;
                margin: 10px 0;
            }
        }

        /* Event Log */
        .log-box {
            background: #090d16;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px;
            max-height: 180px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.76rem;
            word-break: break-word;
        }

        @media (min-width: 768px) {
            .log-box {
                padding: 12px;
                max-height: 220px;
                font-size: 0.8rem;
            }
        }

        .log-item {
            padding: 4px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: #94a3b8;
        }

        .log-item .tag {
            color: var(--accent);
            font-weight: bold;
        }

        /* Variability Groups */
        .variability-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 16px;
        }

        .variability-group-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        .variability-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
        }

        @media (min-width: 480px) {
            .variability-grid {
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 10px;
            }
        }

        .variability-grid .btn {
            width: 100%;
            justify-content: center;
            text-align: center;
            padding: 10px 12px;
            font-size: 0.86rem;
            min-height: 42px;
        }

        /* Timer Grid */
        .timer-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-top: 10px;
        }

        @media (min-width: 480px) {
            .timer-grid {
                grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
                gap: 8px;
            }
        }

        .btn-timer {
            padding: 8px 6px;
            font-size: 0.82rem;
            justify-content: center;
            width: 100%;
            min-height: 40px;
        }
    </style>
</head>
<body>

<div class="container">
    <header>
        <div class="header-title">
            <h2>🏋️‍♂️ GymFit Agent</h2>
            <span class="badge" id="apiStatus">🟢 API Online</span>
        </div>
        <div class="header-actions">
            <button class="btn btn-secondary" onclick="seedDemoData()">⚡ Cargar Caso Demo</button>
            <button class="btn btn-secondary" onclick="resetState()">🔄 Reiniciar Estado</button>
            <a href="/docs" target="_blank" class="btn" style="text-decoration: none;">📖 Ver Swagger Docs</a>
        </div>
    </header>

    <div class="grid-2">
        <!-- Panel 1: Perfil y Equipo -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">1. Perfil del Atleta y Equipo</div>
                <button class="btn" style="padding: 6px 12px;" onclick="saveProfileAndEquipment()">Guardar</button>
            </div>

            <div class="form-row-2">
                <div class="form-group">
                    <label>Nombre</label>
                    <input type="text" id="nombre" value="Carlos Mendoza">
                </div>
                <div class="form-group">
                    <label>Sexo</label>
                    <select id="sexo">
                        <option value="masculino">Masculino</option>
                        <option value="femenino">Femenino</option>
                    </select>
                </div>
            </div>

            <div class="form-row-3">
                <div class="form-group">
                    <label>Peso (kg)</label>
                    <input type="number" id="peso" value="76.0" step="0.5">
                </div>
                <div class="form-group">
                    <label>Altura (cm)</label>
                    <input type="number" id="altura" value="178.0">
                </div>
                <div class="form-group">
                    <label>Días / Sem</label>
                    <input type="number" id="dias" value="3" min="1" max="7">
                </div>
            </div>

            <div class="form-row-2">
                <div class="form-group">
                    <label>Objetivo</label>
                    <select id="objetivo">
                        <option value="ganar_musculo">Ganar Músculo</option>
                        <option value="bajar_grasa">Bajar Grasa</option>
                        <option value="mantenimiento">Mantenimiento</option>
                        <option value="fuerza">Fuerza</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Nivel de Experiencia</label>
                    <select id="nivel">
                        <option value="principiante">Principiante</option>
                        <option value="intermedio">Intermedio</option>
                        <option value="avanzado">Avanzado</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label>Equipo Real Disponible (Haz clic para seleccionar)</label>
                <div class="chips-container" id="equipmentChips">
                    <!-- Se cargan dinámicamente -->
                </div>
            </div>

            <button class="btn" style="width: 100%; margin-top: 10px;" onclick="generateRoutine()">
                ✨ Generar Rutina Semanal con el Agente
            </button>
        </div>

        <!-- Panel 2: Adaptaciones en Vivo e Imprevistos -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">2. Adaptaciones en Tiempo Real (Variabilidad)</div>
            </div>

            <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px;">
                Simula eventos del día a día. El motor funcional puro reajustará el plan sin reiniciarlo:
            </p>

            <div class="variability-container">
                <!-- Grupo 1: Molestias -->
                <div class="variability-group">
                    <div class="variability-group-title">Molestias</div>
                    <div class="variability-grid">
                        <button class="btn btn-warning" onclick="reportDiscomfort('hombro', 6)">
                            🩹 Molestia en Hombro
                        </button>
                        <button class="btn btn-warning" onclick="reportDiscomfort('rodilla', 6)">
                            🩹 Molestia en Rodilla
                        </button>
                    </div>
                </div>

                <!-- Grupo 2: Ajustes de rendimiento -->
                <div class="variability-group">
                    <div class="variability-group-title">Ajustes de rendimiento</div>
                    <div class="variability-grid">
                        <button class="btn btn-secondary" onclick="reportDifficulty('muy_facil')">
                            📈 Sobrecarga (+2.5% Fácil)
                        </button>
                        <button class="btn btn-danger" onclick="reportDifficulty('muy_pesado')">
                            📉 Descarga (-10% Pesado)
                        </button>
                    </div>
                </div>

                <!-- Grupo 3: Imprevistos -->
                <div class="variability-group">
                    <div class="variability-group-title">Imprevistos</div>
                    <div class="variability-grid">
                        <button class="btn btn-secondary" onclick="reportTimeCrunch(2, 25)">
                            ⏱️ Falta de Tiempo (25 min Día 2)
                        </button>
                    </div>
                </div>
            </div>

            <div class="timer-box">
                <div style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">CRONÓMETRO DE DESCANSO ENTRE SERIES</div>
                <div class="timer-display" id="timerDisplay">00:00</div>
                <div class="timer-grid">
                    <button class="btn btn-timer" onclick="startTimer(120)">⏱️ 2:00</button>
                    <button class="btn btn-timer" onclick="startTimer(150)">⏱️ 2:30</button>
                    <button class="btn btn-timer" onclick="startTimer(180)">⏱️ 3:00</button>
                    <button class="btn btn-timer" onclick="startTimer(210)">⏱️ 3:30</button>
                    <button class="btn btn-timer" onclick="startTimer(240)">⏱️ 4:00</button>
                    <button class="btn btn-danger btn-timer" onclick="stopTimer()">⏹️ Detener</button>
                </div>
            </div>

            <div style="margin-top: 18px;">
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 6px; font-weight: 600;">
                    HISTORIAL DE EVENTOS INMUTABLES (Event Sourcing)
                </div>
                <div class="log-box" id="eventLogs">
                    <div class="log-item">Esperando primer evento...</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Panel 3: Rutina Generada y Explicación del Agente -->
    <div class="card">
        <div class="card-header">
            <div class="card-title">3. Rutina Semanal Activa y Justificación del Agente</div>
            <span class="badge" id="routineSplitBadge">Sin Rutina</span>
        </div>

        <div class="agent-bubble" id="agentExplanation">
            Genera una rutina o haz clic en "Cargar Caso Demo" para ver la justificación contextual del agente.
        </div>

        <div id="routineContainer">
            <!-- Días y ejercicios -->
        </div>
    </div>
</div>

<script>
    const ALL_EQUIPMENT = [
        "mancuernas", "banco_plano", "banco_inclinado", "barra", 
        "barra_dominadas", "polea", "maquina_pecho", "maquina_remo",
        "maquina_prensa", "maquina_extensiones", "maquina_curl_femoral", "peso_corporal"
    ];
    let selectedEquipment = new Set(["mancuernas", "banco_plano", "barra_dominadas", "peso_corporal"]);
    let timerInterval = null;

    // Inicializar Chips de Equipo
    function renderChips() {
        const container = document.getElementById("equipmentChips");
        container.innerHTML = "";
        ALL_EQUIPMENT.forEach(eq => {
            const chip = document.createElement("div");
            chip.className = "chip" + (selectedEquipment.has(eq) ? " selected" : "");
            chip.innerText = eq.replace(/_/g, " ");
            chip.onclick = () => {
                if (selectedEquipment.has(eq)) {
                    selectedEquipment.delete(eq);
                } else {
                    selectedEquipment.add(eq);
                }
                renderChips();
            };
            container.appendChild(chip);
        });
    }

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

    // API Calls
    async function saveProfileAndEquipment() {
        const profileData = {
            nombre: document.getElementById("nombre").value,
            sexo: document.getElementById("sexo").value,
            peso_kg: parseFloat(document.getElementById("peso").value),
            altura_cm: parseFloat(document.getElementById("altura").value),
            objetivo: document.getElementById("objetivo").value,
            nivel: document.getElementById("nivel").value,
            dias_disponibles: parseInt(document.getElementById("dias").value)
        };

        await fetch("/api/profile", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(profileData)
        });

        await fetch("/api/equipment", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ equipo: Array.from(selectedEquipment) })
        });

        fetchState();
    }

    async function generateRoutine() {
        await saveProfileAndEquipment();
        const res = await fetch("/api/routine/generate", { method: "POST" });
        if (res.ok) {
            fetchState();
        } else {
            const err = await res.json();
            alert("Error: " + err.detail);
        }
    }

    async function reportDiscomfort(zona, intensidad) {
        const res = await fetch("/api/adjustments/discomfort", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                zona_articular: zona,
                intensidad_1_a_10: intensidad
            })
        });
        if (res.ok) fetchState();
    }

    async function reportTimeCrunch(dia, minutos) {
        const res = await fetch("/api/adjustments/time-crunch", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                tipo: "poco_tiempo",
                dia_afectado: dia,
                minutos_disponibles_hoy: minutos,
                detalle: "Reunión imprevista de trabajo"
            })
        });
        if (res.ok) fetchState();
    }

    async function reportDifficulty(percepcion) {
        const res = await fetch("/api/adjustments/difficulty", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                ejercicio_id: "remo_unilateral_mancuerna",
                percepcion: percepcion,
                comentarios: "Feedback desde panel interactivo"
            })
        });
        if (res.ok) fetchState();
    }

    async function seedDemoData() {
        const res = await fetch("/api/state/seed", { method: "POST" });
        if (res.ok) {
            selectedEquipment = new Set(["mancuernas", "banco_plano", "barra_dominadas", "peso_corporal"]);
            renderChips();
            fetchState();
        }
    }

    async function resetState() {
        await fetch("/api/state/reset", { method: "POST" });
        fetchState();
    }

    async function fetchState() {
        const res = await fetch("/api/state");
        const data = await res.json();
        const state = data.state;

        // Actualizar Rutina
        const rContainer = document.getElementById("routineContainer");
        const expBox = document.getElementById("agentExplanation");
        const splitBadge = document.getElementById("routineSplitBadge");

        if (state.rutina_actual) {
            const r = state.rutina_actual;
            splitBadge.innerText = r.nombre_split;
            expBox.innerText = r.explicacion_agente;

            rContainer.innerHTML = "";
            r.dias.forEach(d => {
                let dayHtml = `
                    <div class="day-card">
                        <div class="day-header">
                            <span>📅 DÍA ${d.dia_numero}: ${d.nombre_dia}</span>
                            <span>⏱️ ~${d.duracion_estimada_minutos} min</span>
                        </div>
                `;

                d.slots.forEach((s, idx) => {
                    const ex = s.ejercicio_principal;
                    const p = s.parametros;
                    const alts = s.alternativas.map(a => a.nombre).join(", ") || "Ninguna alternativa adicional";

                    const techText = (Array.isArray(ex.instrucciones_fijas) && ex.instrucciones_fijas.length > 0)
                        ? ex.instrucciones_fijas.join(" ")
                        : (ex.instrucciones_fijas || "Seguir rango completo y técnica estricta.");
                    const patronText = ex.patron_movimiento ? ex.patron_movimiento.replace(/_/g, " ") : "general";
                    const riesgoText = ex.nivel_riesgo ? ex.nivel_riesgo : "bajo";
                    const articText = (Array.isArray(ex.articulaciones_comprometidas) && ex.articulaciones_comprometidas.length > 0)
                        ? ex.articulaciones_comprometidas.join(", ")
                        : "ninguna articulación crítica";
                    const erroresText = (Array.isArray(ex.errores_comunes) && ex.errores_comunes.length > 0)
                        ? ex.errores_comunes.join(" • ")
                        : "ninguno documentado";
                    const precText = (Array.isArray(ex.precauciones_seguridad) && ex.precauciones_seguridad.length > 0)
                        ? ex.precauciones_seguridad.join(" • ")
                        : "mantener control durante todo el rango de movimiento";

                    dayHtml += `
                        <div class="exercise-item">
                            <div class="exercise-name">
                                <span>${idx + 1}. ${ex.nombre}</span>
                                <span style="color: var(--accent); font-size: 0.85rem; font-weight: 600;">[${s.grupo_muscular.toUpperCase()}]</span>
                            </div>
                            <div class="exercise-line">
                                📊 <strong>Prescripción:</strong> ${p.series} series × ${p.repeticiones_sugeridas} reps | Carga sugerida: ${p.peso_kg_sugerido} kg | Descanso: ${p.descanso_segundos}s
                            </div>
                            <div class="exercise-line">
                                🎯 <strong>Patrón de movimiento:</strong> ${patronText}
                            </div>
                            <div class="exercise-line">
                                ⚠️ <strong>Nivel de riesgo:</strong> ${riesgoText}
                            </div>
                            <div class="exercise-line">
                                🦴 <strong>Articulaciones comprometidas:</strong> ${articText}
                            </div>
                            <div class="exercise-line">
                                💡 <strong>Técnica fija:</strong> ${techText}
                            </div>
                            <div class="exercise-line">
                                ❌ <strong>Errores comunes:</strong> ${erroresText}
                            </div>
                            <div class="exercise-line">
                                🛡️ <strong>Precauciones de seguridad:</strong> ${precText}
                            </div>
                            <div class="exercise-line">
                                🔄 <strong>Alternativas viables:</strong> ${alts}
                            </div>
                        </div>
                    `;
                });

                dayHtml += `</div>`;
                rContainer.innerHTML += dayHtml;
            });
        } else {
            splitBadge.innerText = "Sin Rutina";
            expBox.innerText = "Aún no se ha generado una rutina.";
            rContainer.innerHTML = "<p style='color: var(--text-secondary);'>Configura el perfil y haz clic en 'Generar Rutina'.</p>";
        }

        // Actualizar Logs de Eventos
        const logBox = document.getElementById("eventLogs");
        const evRes = await fetch("/api/state/events");
        const evData = await evRes.json();
        logBox.innerHTML = "";
        evData.eventos.slice().reverse().forEach(ev => {
            logBox.innerHTML += `
                <div class="log-item">
                    <span class="tag">[${ev.tipo}]</span> ${JSON.stringify(ev.datos).slice(0, 100)}...
                </div>
            `;
        });
    }

    // Inicio
    renderChips();
    fetchState();
</script>

</body>
</html>
"""
