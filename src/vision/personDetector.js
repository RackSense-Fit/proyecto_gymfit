/**
 * personDetector.js
 * Módulo puro para detectar si hay una persona en un conjunto de detecciones
 * de un modelo de visión por computadora (ej. COCO-SSD, YOLOv8).
 *
 * SIN efectos secundarios: no toca DOM, canvas, red ni modelos.
 * Solo recibe datos y devuelve datos.
 */

// ─── Configuración ────────────────────────────────────────────────────────────

/** Clase que identifica a una persona en el vocabulario COCO. */
const CLASE_PERSONA = "person";

/**
 * Puntuación mínima de confianza para considerar una detección válida.
 * Rango: [0.0 – 1.0]. Valor inicial conservador para reducir falsos positivos.
 * Cambiar aquí afecta a todo el módulo; no usar números mágicos en el código.
 */
const UMBRAL_DEFAULT = 0.40;

// ─── Tipos (JSDoc) ────────────────────────────────────────────────────────────

/**
 * @typedef {Object} Deteccion
 * @property {string} class  - Clase predicha por el modelo (ej. "person", "car").
 * @property {number} score  - Confianza en [0, 1].
 * @property {number[]} bbox - Bounding box [x, y, width, height] en píxeles.
 */

/**
 * @typedef {Object} ResultadoDeteccion
 * @property {boolean} hayPersona - true si al menos una detección supera el umbral.
 * @property {number}  maxScore   - Score más alto entre detecciones de clase "person"
 *                                  con score >= umbral. 0 si no hay ninguna.
 */

// ─── Función principal ────────────────────────────────────────────────────────

/**
 * Decide si hay al menos una persona en la lista de detecciones,
 * comparando el score de cada detección de clase "person" contra el umbral.
 *
 * La función es pura: mismo input → mismo output, sin efectos secundarios.
 *
 * @param {Deteccion[]} detecciones - Array de objetos {class, score, bbox}.
 * @param {number} [umbral=UMBRAL_DEFAULT] - Confianza mínima para contar una detección.
 * @returns {ResultadoDeteccion}
 */
function decidirSiHayPersona(detecciones, umbral = UMBRAL_DEFAULT) {
  const personasValidas = detecciones.filter(
    (d) => d.class === CLASE_PERSONA && d.score >= umbral
  );

  const hayPersona = personasValidas.length > 0;

  const maxScore = hayPersona
    ? Math.max(...personasValidas.map((d) => d.score))
    : 0;

  return { hayPersona, maxScore };
}

// ─── Exports (CommonJS para compatibilidad con node --test sin bundler) ───────
module.exports = { decidirSiHayPersona, UMBRAL_DEFAULT, CLASE_PERSONA };
