/**
 * nav.test.js
 * Suite de tests para seccionDesdeHash() usando node --test (built-in, v18+).
 */
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { seccionDesdeHash } = require("../../src/api/static/js/nav");

const SECCIONES = ["equipo", "rutina", "entrenar", "calendario"];
const DEFAULT = "equipo";

// ── Hash vacío o ausente ──────────────────────────────────────────────────────

test("Hash vacío '' → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash("", SECCIONES, DEFAULT), "equipo");
});

test("Hash solo '#' → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash("#", SECCIONES, DEFAULT), "equipo");
});

test("Hash undefined → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash(undefined, SECCIONES, DEFAULT), "equipo");
});

test("Hash null → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash(null, SECCIONES, DEFAULT), "equipo");
});

// ── Hash válido ───────────────────────────────────────────────────────────────

test("'#equipo' → 'equipo'", () => {
    assert.strictEqual(seccionDesdeHash("#equipo", SECCIONES, DEFAULT), "equipo");
});

test("'equipo' sin # → 'equipo'", () => {
    assert.strictEqual(seccionDesdeHash("equipo", SECCIONES, DEFAULT), "equipo");
});

test("'#rutina' → 'rutina'", () => {
    assert.strictEqual(seccionDesdeHash("#rutina", SECCIONES, DEFAULT), "rutina");
});

test("'#entrenar' → 'entrenar'", () => {
    assert.strictEqual(seccionDesdeHash("#entrenar", SECCIONES, DEFAULT), "entrenar");
});

test("'#calendario' → 'calendario'", () => {
    assert.strictEqual(seccionDesdeHash("#calendario", SECCIONES, DEFAULT), "calendario");
});

// ── Hash inválido ─────────────────────────────────────────────────────────────

test("'#inexistente' → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash("#inexistente", SECCIONES, DEFAULT), "equipo");
});

test("'#settings' → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash("#settings", SECCIONES, DEFAULT), "equipo");
});

// ── Mayúsculas / minúsculas ───────────────────────────────────────────────────

test("'#EQUIPO' (mayúsculas) → normaliza a 'equipo'", () => {
    assert.strictEqual(seccionDesdeHash("#EQUIPO", SECCIONES, DEFAULT), "equipo");
});

test("'#Rutina' (mixta) → normaliza a 'rutina'", () => {
    assert.strictEqual(seccionDesdeHash("#Rutina", SECCIONES, DEFAULT), "rutina");
});

// ── Sección por defecto distinta ──────────────────────────────────────────────

test("porDefecto personalizado: hash vacío → 'calendario'", () => {
    assert.strictEqual(seccionDesdeHash("", SECCIONES, "calendario"), "calendario");
});

test("porDefecto personalizado: hash inválido → 'calendario'", () => {
    assert.strictEqual(seccionDesdeHash("#nope", SECCIONES, "calendario"), "calendario");
});

// ── Espacios ──────────────────────────────────────────────────────────────────

test("Hash solo espacios '   ' → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash("   ", SECCIONES, DEFAULT), "equipo");
});

test("Hash '#  ' (# + espacios) → devuelve sección por defecto", () => {
    assert.strictEqual(seccionDesdeHash("#  ", SECCIONES, DEFAULT), "equipo");
});
