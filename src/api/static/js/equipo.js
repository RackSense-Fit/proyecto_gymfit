const ALL_EQUIPMENT = [
    "mancuernas", "banco_plano", "banco_inclinado", "barra", 
    "barra_dominadas", "polea", "maquina_pecho", "maquina_remo",
    "maquina_prensa", "maquina_extensiones", "maquina_curl_femoral", "peso_corporal"
];
let selectedEquipment = new Set(["mancuernas", "banco_plano", "barra_dominadas", "peso_corporal"]);

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

// Analizar foto de gimnasio con Gemini Vision y marcar chips automáticamente
async function handleGymPhotoUpload(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    const statusDiv = document.getElementById("visionStatus");
    const btn = document.getElementById("btnUploadGymPhoto");

    if (statusDiv) {
        statusDiv.style.display = "block";
        statusDiv.innerHTML = '<div style="color: var(--accent); font-size: 0.85rem; padding: 6px 0;">⏳ Enviando a Gemini Vision para análisis estructurado...</div>';
    }
    if (btn) btn.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/api/equipment/analyze-image", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error en el análisis de imagen");
        }

        const data = await response.json();

        if (data.equipment_ids && data.equipment_ids.length > 0) {
            data.equipment_ids.forEach(id => selectedEquipment.add(id));
            renderChips();

            if (statusDiv) {
                statusDiv.innerHTML = `
                    <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid var(--success); border-radius: 8px; padding: 10px; margin-top: 6px;">
                        <div style="font-weight: 600; color: var(--success); font-size: 0.85rem; margin-bottom: 3px;">
                            ✨ Equipos detectados: ${data.equipment_ids.map(id => id.replace(/_/g, " ")).join(", ")}
                        </div>
                        <div style="color: var(--text-secondary); font-size: 0.8rem;">${data.resumen || ""}</div>
                    </div>
                `;
            }
        } else {
            if (statusDiv) {
                statusDiv.innerHTML = `
                    <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid var(--warning); border-radius: 8px; padding: 10px; margin-top: 6px;">
                        <div style="color: var(--warning); font-size: 0.85rem;">⚠️ No se detectó equipo específico compatible. Puedes seleccionarlo manualmente.</div>
                    </div>
                `;
            }
        }
    } catch (error) {
        if (statusDiv) {
            statusDiv.innerHTML = `
                <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid var(--danger); border-radius: 8px; padding: 10px; margin-top: 6px;">
                    <div style="color: var(--danger); font-size: 0.85rem;">❌ Error: ${error.message}</div>
                </div>
            `;
        }
    } finally {
        if (btn) btn.disabled = false;
        event.target.value = "";
    }
}
