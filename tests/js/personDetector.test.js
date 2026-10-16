/**
 * personDetector.test.js
 * Suite de tests para decidirSiHayPersona() usando node --test (built-in, v18+).
 * No requiere librerías externas.
 */
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { decidirSiHayPersona, UMBRAL_DEFAULT } = require("../../src/vision/personDetector");

// ── Fixtures reutilizables ────────────────────────────────────────────────────

const personaAlta   = { class: "person", score: 0.92, bbox: [10, 20, 50, 120] };
const personaBaja   = { class: "person", score: 0.20, bbox: [10, 20, 50, 120] };
const personaEnUmbral = { class: "person", score: UMBRAL_DEFAULT, bbox: [0, 0, 60, 140] };
const mancuerna     = { class: "dumbbell", score: 0.85, bbox: [5, 5, 40, 40] };
const kettlebell    = { class: "kettlebell", score: 0.77, bbox: [60, 60, 30, 30] };

// ── Tests ─────────────────────────────────────────────────────────────────────

test("Con una persona con score alto → hayPersona true", () => {
  const resultado = decidirSiHayPersona([personaAlta]);
  assert.strictEqual(resultado.hayPersona, true);
  assert.strictEqual(resultado.maxScore, 0.92);
});

test("Con persona de score bajo (< umbral) → hayPersona false", () => {
  const resultado = decidirSiHayPersona([personaBaja]);
  assert.strictEqual(resultado.hayPersona, false);
  assert.strictEqual(resultado.maxScore, 0);
});

test("Score exactamente igual al umbral → se cuenta como válida (>=)", () => {
  const resultado = decidirSiHayPersona([personaEnUmbral]);
  assert.strictEqual(resultado.hayPersona, true);
  assert.strictEqual(resultado.maxScore, UMBRAL_DEFAULT);
});

test("Lista vacía → hayPersona false, maxScore 0", () => {
  const resultado = decidirSiHayPersona([]);
  assert.strictEqual(resultado.hayPersona, false);
  assert.strictEqual(resultado.maxScore, 0);
});

test("Solo otras clases (sin persona) → hayPersona false", () => {
  const resultado = decidirSiHayPersona([mancuerna, kettlebell]);
  assert.strictEqual(resultado.hayPersona, false);
  assert.strictEqual(resultado.maxScore, 0);
});

test("Múltiples personas → maxScore es el mayor de las válidas", () => {
  const persona2 = { class: "person", score: 0.75, bbox: [100, 0, 50, 140] };
  const resultado = decidirSiHayPersona([personaAlta, persona2]);
  assert.strictEqual(resultado.hayPersona, true);
  assert.strictEqual(resultado.maxScore, 0.92);
});

test("Mezcla de persona válida, persona baja y otras clases → detecta la válida", () => {
  const resultado = decidirSiHayPersona([personaBaja, mancuerna, personaAlta]);
  assert.strictEqual(resultado.hayPersona, true);
  assert.strictEqual(resultado.maxScore, 0.92);
});

test("Umbral personalizado 0.95 → persona con 0.92 no cuenta", () => {
  const resultado = decidirSiHayPersona([personaAlta], 0.95);
  assert.strictEqual(resultado.hayPersona, false);
  assert.strictEqual(resultado.maxScore, 0);
});

test("Umbral personalizado 0.10 → persona con score 0.20 sí cuenta", () => {
  const resultado = decidirSiHayPersona([personaBaja], 0.10);
  assert.strictEqual(resultado.hayPersona, true);
  assert.strictEqual(resultado.maxScore, 0.20);
});
