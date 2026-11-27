/**
 * nav.js — Navegación por pestañas con hash routing.
 *
 * Función pura: seccionDesdeHash (sin acceso a DOM ni entorno).
 * Frontera (DOM): activarSeccion, irASeccion, listeners.
 *
 * Patrón de exportación dual (Node / browser).
 */

// ── Función pura ──────────────────────────────────────────────────────────────

/**
 * Dada una cadena de hash, devuelve el nombre de sección válido o el default.
 * @param {string} hash - Valor del hash (con o sin "#")
 * @param {string[]} seccionesValidas - Lista de secciones permitidas
 * @param {string} porDefecto - Sección por defecto si hash vacío/inválido
 * @returns {string} Nombre de sección normalizado
 */
function seccionDesdeHash(hash, seccionesValidas, porDefecto) {
    if (typeof hash !== "string" || hash.replace("#", "").trim() === "") {
        return porDefecto;
    }
    const limpio = hash.replace(/^#/, "").toLowerCase();
    if (seccionesValidas.indexOf(limpio) !== -1) {
        return limpio;
    }
    return porDefecto;
}

// ── Frontera DOM ──────────────────────────────────────────────────────────────

if (typeof document !== "undefined") {
    const SECCIONES = ["equipo", "rutina", "entrenar", "calendario"];
    const POR_DEFECTO = "equipo";

    function activarSeccion(nombre) {
        // Mostrar / ocultar secciones
        document.querySelectorAll("section[data-seccion]").forEach(function (sec) {
            if (sec.getAttribute("data-seccion") === nombre) {
                sec.removeAttribute("hidden");
            } else {
                sec.setAttribute("hidden", "");
            }
        });

        // Marcar pestaña activa
        document.querySelectorAll(".nav-tabs a").forEach(function (link) {
            var href = link.getAttribute("href") || "";
            var seccion = href.replace(/^#/, "");
            if (seccion === nombre) {
                link.setAttribute("aria-current", "page");
            } else {
                link.removeAttribute("aria-current");
            }
        });

        window.scrollTo(0, 0);
    }

    function alCambiarHash() {
        var seccion = seccionDesdeHash(location.hash, SECCIONES, POR_DEFECTO);
        activarSeccion(seccion);
    }

    /** Función global para navegar a una sección desde otros scripts. */
    window.irASeccion = function (nombre) {
        location.hash = "#" + nombre;
    };

    window.addEventListener("hashchange", alCambiarHash);
    document.addEventListener("DOMContentLoaded", alCambiarHash);
}

// ── Exportación Node ──────────────────────────────────────────────────────────

if (typeof module !== "undefined" && module.exports) {
    module.exports = { seccionDesdeHash };
}
