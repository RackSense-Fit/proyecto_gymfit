// API Calls - Perfil y Equipo
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
