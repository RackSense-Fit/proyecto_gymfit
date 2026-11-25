// API Calls - Estado y Traza de Eventos
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

// Inicialización de la aplicación
renderChips();
fetchState();
