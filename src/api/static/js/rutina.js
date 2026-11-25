// API Calls - Rutina y Variabilidad
async function generateRoutine() {
    await saveProfileAndEquipment();
    const res = await fetch("/api/routine/generate", { method: "POST" });
    if (res.ok) {
        await fetchState();
    } else {
        const err = await res.json();
        alert("Error: " + (err.detail || "No se pudo generar la rutina"));
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
    if (res.ok) {
        const data = await res.json();
        await fetchState();
        alert("🩹 " + data.message + "\n\n" + data.explicacion_agente);
    } else {
        const err = await res.json();
        alert("⚠️ " + (err.detail || "Debe existir una rutina activa antes de reportar molestias. Haz clic en 'Cargar Datos Demo' o 'Generar Rutina'."));
    }
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
    if (res.ok) {
        const data = await res.json();
        await fetchState();
        alert("⏱️ " + data.message + "\n\n" + data.explicacion_agente);
    } else {
        const err = await res.json();
        alert("⚠️ " + (err.detail || "Debe existir una rutina activa antes de aplicar este imprevisto. Haz clic en 'Cargar Datos Demo' o 'Generar Rutina'."));
    }
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
    if (res.ok) {
        const data = await res.json();
        await fetchState();
        alert("📈 " + data.message + "\n\n" + data.explicacion_agente);
    } else {
        const err = await res.json();
        alert("⚠️ " + (err.detail || "Debe existir una rutina activa antes de ajustar dificultad. Haz clic en 'Cargar Datos Demo' o 'Generar Rutina'."));
    }
}
