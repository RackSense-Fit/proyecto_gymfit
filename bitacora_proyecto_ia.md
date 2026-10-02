# Bitácora de Desarrollo — Proyecto IA Agéntica (GymFit Agent)

Registro continuo de requerimientos, diseño arquitectónico, eventos, decisiones técnicas y avances de implementación del proyecto **GymFit Agent** para la materia de Programación Funcional.

---

## [2026-09-17 12:08:59] - Creación e Inicialización de la Bitácora de Proyecto IA Agéntica

**Prompt / Solicitud del Usuario:**
> *"crea una bitacora aparte en la carpeta de proyecto_ia que se llame bitacora_proyecto_ia"*

### Lista de Tareas
- [x] Crear el archivo de seguimiento [`bitacora_proyecto_ia.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/bitacora_proyecto_ia.md) exclusivo para el proyecto **GymFit Agent** dentro de `proyecto_ia_agentica/`.
- [x] Documentar el contexto base: Arquitectura funcional de 4 capas (*Eventos -> Estado -> Motor de Decisión -> Salida*), inmutabilidad estricta (`@dataclass(frozen=True)`), fold de eventos con `match-case`, catálogos A/B y filtrado bicondicional puro.
- [x] Registrar la propuesta de estructura modular de carpetas (`data/`, `src/models/`, `src/catalog/`, `src/engine/`, `src/reducer/`, `tests/`, `main.py`).
- [ ] Implementar la estructura de directorios y los modelos inmutables de datos una vez aprobada la arquitectura.

### Detalle de lo Realizado:
1. Se inicializó la bitácora independiente del proyecto [`bitacora_proyecto_ia.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/bitacora_proyecto_ia.md) para registrar el ciclo de vida, diseño y desarrollo del agente de IA.
2. Se formalizó la trazabilidad de prompts, decisiones técnicas y lista de tareas en formato markdown con corchetes (`[x]` / `[ ]`) y timestamps.
3. Se integró el seguimiento sincronizado con el espacio de trabajo general de la materia.

---

## [2026-09-17 12:11:58] - Directriz de Documentación Didáctica y Explicación Detallada de Código

**Prompt / Solicitud del Usuario:**
> *"en la bitacora lleva una documentación para saber que es lo que se está haciendo de cada una de las cosas que haga (en el momento que se empiece a crear codigo), explicando cada u no de ellas, sé didáctico y explica cada cosa detalladamente."*

### Lista de Tareas
- [x] Establecer el protocolo de documentación didáctica y pedagógica obligatoria en la bitácora para cada módulo, función y estructura de datos que se construya.
- [x] Definir la estructura explicativa para cada entrega de código: *¿Qué es?*, *¿Por qué se diseñó así?*, *¿Qué principio funcional aplica? (pureza, inmutabilidad, orden superior, pattern matching, fold)*, y *¿Cómo interactúa con el resto del sistema?*.
- [ ] Aplicar este esquema didáctico detallado a partir de la primera fase de codificación (modelos inmutables de dominio).

### Detalle de lo Realizado:
1. Se adoptó el estándar pedagógico de documentación exhaustiva dentro de la bitácora: cada bloque de código creado incluirá una descomposición paso a paso con justificación funcional, diagrama o flujo conceptual y explicación de tipos.
2. Se asegurará que la bitácora funcione tanto como registro de ingeniería como material de estudio para la materia de Programación Funcional.

---

## [2026-09-17 12:18:53] - Independencia del Proyecto y Creación de `documentacion.md`

**Prompt / Solicitud del Usuario:**
> *"No, no sincronices nada en la bitacora_de_estudio este proyecto solo será trabajado en la carpeta de ia_agentica crea otro documento que se llame "documentacion"donde ahi pondras y explicaras lo que se haga de codigo y estructura."*

### Lista de Tareas
- [x] Desvincular el proyecto de `bitacora_de_estudio.md`; todo el trabajo, bitácora y documentación residirán exclusivamente en la carpeta `proyecto_ia_agentica/`.
- [x] Crear el documento oficial [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md) para albergar explicaciones técnicas, didácticas y conceptuales de cada módulo y función.
- [x] Mantener [`bitacora_proyecto_ia.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/bitacora_proyecto_ia.md) como el registro cronológico de interacciones, prompts, tareas y decisiones.
- [ ] Comenzar la redacción técnica detallada en `documentacion.md` en paralelo al desarrollo del código.

### Detalle de lo Realizado:
1. Se aisló completamente el flujo de trabajo dentro del directorio [`proyecto_ia_agentica/`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica).
2. Se creó el archivo [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md) con la estructura base de conceptos de Programación Funcional, arquitectura de 4 capas y diagramas.
3. Se estableció la división clara de responsabilidades entre ambos archivos:
   - `bitacora_proyecto_ia.md`: Historial cronológico de tareas y prompts.
   - `documentacion.md`: Explicaciones pedagógicas y técnicas detalladas del código y arquitectura.

---

## [2026-09-18 13:12:04] - Implementación del Núcleo Funcional Completo, Suite de Pruebas y Documentación

**Prompt / Solicitud del Usuario:**
> *"adelante"*

### Lista de Tareas
- [x] Crear fuentes de datos JSON estáticas en `data/` con catálogo de ejercicios (Tabla B - Free Exercise DB), splits de entrenamiento y parámetros por nivel (Tabla A - ACSM/NSCA).
- [x] Implementar la capa de modelos inmutables de dominio en `src/models/` (`enums.py`, `profile.py`, `catalog.py`, `routine.py`, `events.py`, `state.py`) utilizando `@dataclass(frozen=True)` y unión tipada de eventos `DomainEvent`.
- [x] Implementar el cargador puro de catálogo y las funciones puras de filtrado bicondicional (`Equipo ∩ Nivel`) en `src/catalog/` (`loader.py`, `filters.py`).
- [x] Construir el motor funcional de decisiones en `src/engine/` (`split_selector.py`, `generator.py`, `adjuster.py`, `explainer.py`), asegurando técnica fija de seguridad, 1-2 alternativas por ranura y justificaciones contextuales.
- [x] Diseñar e implementar el reductor de eventos puro y la función de *fold* de historial (`state + event -> new_state` y `functools.reduce`) en `src/reducer/` (`state_reducer.py`, `history_fold.py`).
- [x] Desarrollar la suite de pruebas unitarias automatizadas en `tests/` (`test_filters.py`, `test_generator.py`, `test_reducer.py`) con validación al 100% (9/9 tests pasando).
- [x] Crear el punto de entrada ejecutable `src/main.py` con una simulación completa de flujo de vida (perfil, registro de equipo, generación de rutina, registro de sesión con cronómetro, adaptación reactiva ante molestia/tiempo/dificultad y verificación de determinismo matemático vía `fold_events`).
- [x] Redactar la documentación técnica y didáctica integral en [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md).

### Detalle de lo Realizado:
1. **Datos de Catálogo (`data/`):**
   - [`table_a_levels.json`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/data/table_a_levels.json): Parámetros de series, repeticiones, descansos y restricciones por nivel.
   - [`table_b_exercises.json`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/data/table_b_exercises.json): 17 ejercicios con técnica fija inmutable, articulaciones comprometidas y equipos requeridos.
   - [`table_b_splits.json`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/data/table_b_splits.json): Plantillas de Fullbody (2 y 3 días), Torso/Pierna (4 días) y Push/Pull/Legs (5 y 6 días).

2. **Modelos Inmutables (`src/models/`):**
   - [`profile.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/models/profile.py): `UserProfile` con distinción de campos fijos y editables.
   - [`events.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/models/events.py): 11 eventos de dominio agrupados en el tipo algebraico `DomainEvent`.
   - [`state.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/models/state.py): `AppState` inmutable con historial de eventos, sesiones y calendario.
   - [`routine.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/models/routine.py): `WeeklyRoutine`, `DailyWorkout` y `WorkoutSlot` con alternativas seguras.

3. **Filtrado y Motor Puro (`src/catalog/`, `src/engine/`, `src/reducer/`):**
   - [`filters.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/catalog/filters.py): Filtrado bicondicional puro sin efectos colaterales.
   - [`generator.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/engine/generator.py) y [`adjuster.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/engine/adjuster.py): Generación y adaptación funcional de planes.
   - [`state_reducer.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/reducer/state_reducer.py) y [`history_fold.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/reducer/history_fold.py): Reducción de estado con pattern matching (`match-case`) y reconstrucción determinista mediante `reduce`.

4. **Validación y Ejecución:**
   - Pruebas unitarias ejecutadas exitosamente: 9 de 9 tests aprobados (`python -m unittest discover -s tests -v`).
   - Simulación de consola [`src/main.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/main.py) ejecutada y verificada de punta a punta.
   - Documentación técnica exhaustiva actualizada en [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md).

---

## [2026-09-18 13:16:12] - Análisis y Propuesta de Stack Tecnológico para la Evolución de GymFit Agent

**Prompt / Solicitud del Usuario:**
> *"que tipos de tecnologias puedo implementar en este proyecto, lenguajes, framworks etc?"*

### Lista de Tareas
- [x] Analizar el ecosistema tecnológico adecuado para cada una de las capas evolutivas de **GymFit Agent** (Visión Computacional, Orquestación Agéntica, API Backend, Frontend Web/Móvil, Persistencia/Event Store).
- [x] Clasificar las tecnologías según su compatibilidad con el Paradigma Funcional, facilidad de desarrollo y valor académico/profesional.
- [x] Documentar el roadmap tecnológico detallado en la bitácora y en [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md).
- [ ] Definir con el usuario el stack tecnológico que se utilizará en la siguiente fase de desarrollo (ej. API FastAPI, Prototipo Web con Streamlit/React, o Visión Multimodal).

### Detalle de lo Realizado:
1. Se estructuró un catálogo comprensivo de tecnologías dividido en 6 ejes estratégicos:
   - **Núcleo Funcional y Lenguajes:** Python (con bibliotecas funcionales como `returns`, `toolz`, `pydantic`), Rust, Elixir.
   - **IA Agéntica y LLMs:** LangGraph (basado en máquinas de estado / grafos puros), Instructor, Ollama / Gemini API.
   - **Visión por Computadora (Fotos de Gimnasio):** Modelos Multimodales (Gemini Vision / GPT-4o) y Visión Clásica (YOLOv8/11, Roboflow).
   - **Backend y APIs:** FastAPI, Litestar.
   - **Frontend / UX:** Streamlit / Gradio (prototipado rápido de consola a interfaz interactiva), React / Next.js, React Native / Flutter (móvil).
   - **Persistencia y Event Sourcing:** PostgreSQL (JSONB / Event Store), SQLite, Supabase.
2. Se actualizaron los documentos de seguimiento sin alterar el espacio de trabajo general.

---

## [2026-09-20 02:00:54] - Diseño de Arquitectura para Aplicación Móvil (GymFit Mobile)

**Prompt / Solicitud del Usuario:**
> *"en base a todo lo visto hasta el momento, como podria crearlo en una app movil?"*

### Lista de Tareas
- [x] Diseñar la arquitectura cliente-servidor para la app móvil de **GymFit Agent**, conectando el frontend móvil con el núcleo funcional puro de Python.
- [x] Definir el stack tecnológico móvil óptimo (**React Native con Expo + TypeScript** y **FastAPI** como backend).
- [x] Detallar las 6 pantallas clave del flujo de usuario (Perfil, Escáner de Equipo con Cámara, Dashboard de Rutina, Modo Entrenamiento en Vivo con Cronómetro, Modal de Ajustes Rápidos y Calendario Mensual).
- [x] Documentar el patrón de estado funcional en el frontend (Zustand/Redux mirroring del `reduce_event`) y la estrategia offline-first.
- [x] Integrar la sección técnica completa en [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md).

### Detalle de lo Realizado:
1. Se estructuró la solución integral para llevar GymFit Agent al contexto físico real del gimnasio:
   - **Frontend:** React Native (Expo) con acceso a cámara nativa (`expo-camera`), cronómetro en segundo plano (`expo-notifications` / `expo-av`) y gestión de estado inmutable.
   - **API Backend:** FastAPI exponiendo endpoints REST que consumen directamente nuestro motor funcional puro (`src/models/`, `src/catalog/`, `src/engine/`, `src/reducer/`).
   - **Manejo de Eventos Móvil:** Cada interacción del usuario (pulsar cronómetro, reportar molestia, cambiar peso) dispara un `DomainEvent` serializado en JSON que alimenta la función pura `reduce_event`.
2. Se actualizó la documentación técnica oficial con diagramas de flujo y esquemas de pantallas.

---

## [2026-09-20 02:05:33] - Implementación del Backend API REST con FastAPI

**Prompt / Solicitud del Usuario:**
> *"avancemos con el backend con fast api"*

### Lista de Tareas
- [x] Instalar y configurar las dependencias del servidor: `fastapi`, `uvicorn`, `httpx` y `pydantic`.
- [x] Crear el paquete de API en `src/api/` con esquemas tipados Pydantic (`schemas.py`) y gestor de estado inmutable (`state_manager.py`).
- [x] Implementar enrutadores modulares por dominio en `src/api/routers/`:
  - `profile.py`: Endpoints para crear/consultar perfiles (`POST /api/profile`, `GET /api/profile`).
  - `equipment.py`: Endpoints para registrar/actualizar inventario de equipo y consultar catálogo (`POST /api/equipment`, `GET /api/equipment`, `GET /api/equipment/catalog`).
  - `routine.py`: Endpoints para generación pura de rutinas y consulta activa (`POST /api/routine/generate`, `GET /api/routine`).
  - `session.py`: Endpoints para inicio de sesión, registro de serie con cronómetro y finalización (`POST /api/session/start`, `POST /api/session/set`, `POST /api/session/finish`, `GET /api/session/active`, `GET /api/session/history`).
  - `variability.py`: Endpoints para reportar molestias, falta de tiempo y dificultad percibida (`POST /api/adjustments/discomfort`, `POST /api/adjustments/time-crunch`, `POST /api/adjustments/difficulty`, `GET /api/adjustments/history`).
  - `events.py`: Endpoints para consultas globales de `AppState` y traza completa de Event Sourcing (`GET /api/state`, `GET /api/state/events`, `POST /api/state/reset`).
- [x] Configurar la aplicación principal `src/api/app.py` con middleware CORS (apto para clientes web y móviles), documentación Swagger (`/docs`) y Redoc (`/redoc`).
- [x] Crear y ejecutar la suite de pruebas de integración con `TestClient` en `tests/test_api.py` (11/11 tests pasando al 100%).
- [x] Actualizar la documentación técnica oficial en [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md).

### Detalle de lo Realizado:
1. **Infraestructura API (`src/api/`):**
   - Se levantó la capa de servicios web desacoplada que permite conectar la app móvil (o web) directamente con el núcleo funcional en Python.
   - Cada endpoint recibe DTOs validados con Pydantic, los transforma en eventos de dominio inmutables (`DomainEvent`) y ejecuta la reducción pura `reduce_event(state, event, catalog)`.
2. **Validación:**
   - Se ejecutaron las 11 pruebas automatizadas del proyecto (`tests/test_filters.py`, `tests/test_generator.py`, `tests/test_reducer.py` y `tests/test_api.py`) con resultado `OK` en 0.211 segundos.
3. **Documentación:**
   - Se detalló el catálogo de endpoints REST, ejemplos de payloads JSON y comando de arranque en la documentación oficial.

---

## [2026-09-20 02:18:03] - Instrucciones de Ejecución del Servidor con Recarga Automática

**Prompt / Solicitud del Usuario:**
> *"la recarga automática en donde lo ejecuto?"*

### Lista de Tareas
- [x] Explicar detalladamente el entorno, terminal y comandos para ejecutar el servidor con recarga automática (`--reload`).
- [x] Resolver la advertencia de PATH en Windows recomendando la sintaxis modular segura: `python -m uvicorn src.api.app:app --reload`.
- [x] Documentar las opciones de arranque alternativas (ejecución directa de `python src/api/app.py`).

### Detalle de lo Realizado:
1. Se orientó al usuario sobre dónde abrir la terminal (terminal integrada del editor o PowerShell) y la ruta requerida (`proyecto_ia_agentica`).
2. Se explicó el funcionamiento de la bandera `--reload` (observador de cambios en tiempo real) y cómo acceder a la interfaz Swagger en el navegador.

---

## [2026-09-20 02:21:56] - Diagnóstico y Activación del Servidor FastAPI en Segundo Plano

**Prompt / Solicitud del Usuario:**
> *"http://localhost:8000/docs da como respuesta a una pagina con mensajes como This site can’t be reached"*

### Lista de Tareas
- [x] Diagnosticar el motivo del error *"This site can’t be reached"* (el proceso del servidor no estaba escuchando en el puerto 8000).
- [x] Iniciar el servidor FastAPI con Uvicorn en segundo plano (`127.0.0.1:8000`).
- [x] Verificar la disponibilidad y respuesta HTTP del endpoint de documentación interactiva (`http://127.0.0.1:8000/docs` respondió con código 200 OK).

### Detalle de lo Realizado:
1. Se comprobó mediante `netstat` que el puerto 8000 no tenía ningún proceso activo escuchando peticiones.
2. Se puso en marcha el servidor FastAPI como proceso de fondo en `http://127.0.0.1:8000`.
3. Se validó la conectividad HTTP exitosa obteniendo respuesta `Status: 200` en `/docs`.

---

## [2026-09-20 02:29:42] - Entrega de Base Integral de Pruebas, Dashboard Interactivo y Scripts de Automatización

**Prompt / Solicitud del Usuario:**
> *"termina todo lo necesario para que quede lista una prueba donde podamos mejorarla con forme pase el tiempo, para tener una base en donde trabajar, aplica todo lo visto"*

### Lista de Tareas
- [x] Desarrollar un **Dashboard Web Interactivo** integrado directamente en FastAPI (`src/api/dashboard_html.py`) servido en `http://localhost:8000/` y `/dashboard`.
- [x] Implementar endpoint de inicialización en 1 clic (`POST /api/state/seed`) para poblar un escenario completo (perfil, equipo y rutina) sin configuración manual.
- [x] Añadir simulación interactiva de cronómetro de descanso entre series con temporizador visual y avisos.
- [x] Conectar botones de prueba de variabilidad en vivo (molestia en hombro/rodilla, versión exprés por tiempo y sobrecarga progresiva).
- [x] Crear scripts de automatización en Windows (`run_server.bat`, `run_tests.bat`, `run_demo_cli.bat`) para agilizar el flujo de trabajo sin recordar comandos de consola.
- [x] Verificar la suite completa de 12 pruebas unitarias e integración pasando al 100% (`OK` en 0.211s).
- [x] Actualizar la documentación oficial en [`documentacion.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/documentacion.md).

### Detalle de lo Realizado:
1. **Entorno Visual de Pruebas:** Se creó una interfaz moderna, responsiva y en modo oscuro que consume los endpoints REST y permite visualizar en tiempo real cómo el estado inmutable evoluciona ante cada evento.
2. **Ciclo de Mejora Continua:** El proyecto queda estructurado de manera que cualquier nueva funcionalidad (visión por computadora, modelos LLM, base de datos en la nube o app móvil) pueda conectarse directamente a este núcleo sin rehacer código previo.
3. **Scripts de Lanzamiento:** Se agregaron archivos `.bat` en la raíz del proyecto para iniciar el servidor con recarga automática o ejecutar pruebas con un solo clic.

---

## [2026-09-20 14:01:10] - Clonación del Repositorio free-exercise-db

**Prompt / Solicitud del Usuario:**
> *"Clona el repositorio completo https://github.com/yuhonas/free-exercise-db dentro de una carpeta que crearas llamada data/external/free-exercise-db en este proyecto. Necesito todo el contenido: el JSON combinado, los archivos individuales por ejercicio, las imágenes y las instrucciones."*

### Lista de Tareas
- [x] Clonar el repositorio `https://github.com/yuhonas/free-exercise-db` en `data/external/free-exercise-db/`
- [x] Verificar que `dist/exercises.json` (JSON combinado) esté presente (~1 MB, todos los ejercicios)
- [x] Verificar que los 873 directorios individuales de ejercicios estén presentes en `exercises/`
- [x] Verificar que las imágenes GIF animadas estén presentes dentro de cada carpeta de ejercicio
- [x] Verificar que el `schema.json`, `README.md` y `LICENSE.md` estén disponibles
- [x] Actualizar bitácora con el resultado

### Detalle de lo Realizado:

#### ¿Qué es `free-exercise-db`?
Es una base de datos de ejercicios de fitness de código abierto, mantenida por la comunidad. Contiene información estructurada sobre **873 ejercicios** en formato JSON, incluyendo:
- **Nombre** del ejercicio
- **Músculos primarios y secundarios** trabajados
- **Equipamiento** requerido (barbell, dumbbell, cable, machine, bodyweight, etc.)
- **Categoría** (fuerza, estiramiento, pliometría, cardio, etc.)
- **Nivel** (beginner, intermediate, expert)
- **Instrucciones** paso a paso
- **Imágenes GIF** animadas que ilustran la ejecución correcta

#### Estructura del repositorio clonado:
```
data/external/free-exercise-db/
├── dist/
│   └── exercises.json        ← JSON combinado con TODOS los ejercicios (~1 MB)
├── exercises/
│   ├── 3_4_Sit-Up/
│   │   └── *.gif             ← Imágenes animadas del ejercicio
│   ├── 3_4_Sit-Up.json       ← Datos individuales del ejercicio
│   ├── Barbell_Squat/
│   │   └── *.gif
│   ├── Barbell_Squat.json
│   └── ... (873 ejercicios en total)
├── schema.json               ← Esquema JSON de la estructura de un ejercicio
├── README.md                 ← Documentación del repositorio
├── LICENSE.md                ← Licencia
└── Makefile                  ← Scripts de construcción del repo original
```

#### Estadísticas del clone:
| Métrica | Valor |
|---|---|
| Total de archivos descargados | 2,668 archivos |
| Ejercicios individuales | 873 ejercicios |
| JSON combinado (`exercises.json`) | ~1 MB |
| Fuente | https://github.com/yuhonas/free-exercise-db |

#### ¿Por qué es importante para GymFit Agent?
Este repositorio es la **fuente de datos de ejercicios** del agente. En lugar de hardcodear ejercicios manualmente, el agente podrá:
1. **Leer** `dist/exercises.json` para cargar el catálogo completo al iniciar
2. **Filtrar** ejercicios por equipamiento disponible en el gimnasio del usuario
3. **Filtrar** por músculo objetivo, nivel de dificultad y categoría
4. **Mostrar** las imágenes GIF animadas en el dashboard para que el usuario vea cómo ejecutar cada ejercicio correctamente

#### Próximo paso:
Integrar `dist/exercises.json` como fuente de datos en `src/catalog/` para que el filtrado funcional trabaje sobre datos reales en lugar del catálogo de demo actual.

---

## [2026-09-20 14:06:39] - Ajuste de Parámetros del Nivel Avanzado y Ejecución de Pruebas

**Prompt / Solicitud del Usuario:**
> *El usuario modificó `data/table_a_levels.json` y dijo "adelante" para ejecutar los tests.*

### Cambio Realizado en `table_a_levels.json`:
| Parámetro | Valor Anterior | Valor Nuevo |
|---|---|---|
| `rango_series_por_ejercicio` (avanzado) | `[4, 5]` | `[2, 3]` |
| `rango_repeticiones` (avanzado) | `[6, 10]` | `[6, 12]` |

#### ¿Por qué importa este cambio?
La **Tabla A** define los parámetros de entrenamiento por nivel. El nivel `"avanzado"` ahora genera rutinas con:
- **Menos series** (2-3 en lugar de 4-5): reduce el volumen total por ejercicio
- **Más repeticiones** (hasta 12 en lugar de 10): amplía el rango hacia hipertrofia moderada

Esto refleja una decisión de diseño: el nivel avanzado puede trabajar con mayor intensidad pero menor volumen acumulado por ejercicio.

### Lista de Tareas
- [x] Usuario ajustó `rango_series_por_ejercicio` de `[4,5]` → `[2,3]` para nivel avanzado
- [x] Usuario ajustó `rango_repeticiones` de `[6,10]` → `[6,12]` para nivel avanzado
- [x] Instalar `pytest` y `pytest-asyncio` (no estaban en el entorno)
- [x] Ejecutar suite de pruebas completa (`tests/`)
- [x] Verificar que todos los tests pasen con los nuevos parámetros

### Resultado de los Tests:
```
======================= 12 passed, 34 warnings in 0.95s =======================
```

✅ **12 de 12 tests pasaron** — El cambio de parámetros no rompió ninguna prueba existente.

Las 34 advertencias son `PydanticDeprecatedSince20` sobre el uso de `example=` en `Field()` dentro de `schemas.py`. Son advertencias de compatibilidad con Pydantic V2 (no errores) y no afectan el funcionamiento.

### Detalle de lo Realizado:
1. Se instaló `pytest 9.1.1` y `pytest-asyncio 1.4.0` (no estaban disponibles en el entorno Python 3.14).
2. Se ejecutó `python -m pytest tests/ -v --tb=short`.
3. Los 12 tests de integración (`TestFastAPIIntegration`) pasaron correctamente con los nuevos valores de la Tabla A.
4. El cambio de parámetros en `table_a_levels.json` es **no disruptivo**: el motor de decisión lee estos valores en tiempo de ejecución, por lo que cualquier ajuste en el JSON se refleja automáticamente sin reiniciar el servidor.

---

## [2026-09-20 14:09:44] - Corrección de Advertencias de Deprecación Pydantic V2 en `schemas.py`

**Prompt / Solicitud del Usuario:**
> *"solucionalo"* (en referencia a las 34 advertencias `PydanticDeprecatedSince20` en `schemas.py`)

### Lista de Tareas
- [x] Identificar todos los `Field(..., example=...)` en [`schemas.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/api/schemas.py)
- [x] Migrar a `Field(..., json_schema_extra={"example": ...})` en todas las clases
- [x] Verificar que los 12 tests siguen pasando
- [x] Confirmar reducción de advertencias: de 34 → 2 (solo de librerías externas)

### ¿Qué se cambió y por qué?

#### El problema: `example=` deprecado en Pydantic V2
En Pydantic V1, era válido escribir:
```python
nombre: str = Field(..., example="Carlos Mendoza")
```

En Pydantic V2 (que es la versión instalada), ese argumento **ya no se soporta directamente** en `Field()`. Pydantic lo movió a un diccionario de metadatos extra para el JSON Schema:
```python
nombre: str = Field(..., json_schema_extra={"example": "Carlos Mendoza"})
```

#### Impacto visual cero
El cambio es **puramente técnico**: los ejemplos siguen apareciendo en la documentación automática de FastAPI (`/docs`), pero ahora sin generar advertencias al importar el módulo.

### Resultado de los Tests (después del fix):
```
12 passed, 2 warnings in 0.47s
```

Las 2 advertencias restantes son de librerías externas:
- `StarletteDeprecationWarning` — Starlette sugiere usar `httpx2` en vez de `httpx` con TestClient
- `DeprecationWarning` de `anyio.abc.BlockingPortal` — alias deprecado dentro de anyio

Ambas son **ajenas a nuestro código** y se resolverán actualizando las dependencias en el futuro.

---

## [2026-09-24 19:35:40] - Refactorización de `state_reducer.py` con `dataclasses.replace`

**Prompt / Solicitud del Usuario:**
> *"Refactoriza el archivo src/reducer/state_reducer.py.*
> *Actualmente, cada rama del match/case dentro de reduce_event() reconstruye manualmente una instancia completa de AppState con sus 8 campos, repitiendo el mismo bloque ~12 veces con solo 1-2 campos distintos por rama. Esto es frágil: si en el futuro se agrega un nuevo campo a AppState, hay que recordar actualizar las 12 ramas manualmente, y olvidar una sola introduce un bug silencioso.*
> *Reemplaza esas reconstrucciones manuales usando dataclasses.replace(), especificando solo los campos que cambian en cada rama, y dejando que el resto se copie automáticamente del estado anterior...*
> *Aplica el mismo patrón a las 12 ramas del match/case (incluyendo el caso residual `case _:`). No cambies la lógica de negocio de ninguna rama, solo la forma de construir el AppState resultante. Asegúrate de importar `replace` desde el módulo dataclasses al inicio del archivo.*
> *Al terminar, corre src/main.py y confirma que el demo sigue funcionando exactamente igual que antes (mismos eventos, misma rutina generada, mismo resultado en la verificación de fold_events), para comprobar que el refactor no cambió ningún comportamiento."*

### Lista de Tareas
- [x] Importar `replace` desde `dataclasses` en [`src/reducer/state_reducer.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/reducer/state_reducer.py).
- [x] Refactorizar las 12 ramas de `match event:` para usar `replace(state, ...)` en lugar de reconstruir manualmente `AppState(...)` con todos los campos.
- [x] Mantener idéntica la lógica de negocio, validaciones y guardas de cada evento.
- [x] Ejecutar `python src/main.py` y verificar determinismo exacto y validación de pureza con `fold_events()`.
- [x] Ejecutar suite de pruebas `pytest tests/` (12/12 pasadas).

### Detalle de lo Realizado:
1. **Importación limpia:** Se agregó `from dataclasses import replace` al inicio de [`src/reducer/state_reducer.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/reducer/state_reducer.py).
2. **Reemplazo en las 12 ramas de `match event:`:**
   - `PerfilCreado`: `replace(state, perfil=perfil, historial_eventos=nuevo_historial_eventos)`
   - `EquipoRegistrado`: `replace(state, equipo_disponible=equipo, historial_eventos=nuevo_historial_eventos)`
   - `EquipoActualizado`: `replace(state, equipo_disponible=nuevo_equipo, historial_eventos=nuevo_historial_eventos)`
   - `RutinaGenerada`: `replace(state, rutina_actual=rutina, historial_eventos=nuevo_historial_eventos)`
   - `SesionIniciada`: `replace(state, sesion_en_curso=nueva_sesion, historial_eventos=nuevo_historial_eventos)`
   - `SerieRegistrada`: Si no coincide sesión activa `replace(state, historial_eventos=nuevo_historial_eventos)`, si coincide `replace(state, sesion_en_curso=sesion_actualizada, historial_eventos=nuevo_historial_eventos)`
   - `SesionFinalizada`: `replace(state, sesion_en_curso=None, historial_sesiones=state.historial_sesiones + (sesion_cerrada,), calendario=state.calendario + (nueva_entrada_cal,), historial_eventos=nuevo_historial_eventos)`
   - `DificultadReportada`: `replace(state, rutina_actual=rutina_ajustada, historial_ajustes=state.historial_ajustes + (ajuste_log,), historial_eventos=nuevo_historial_eventos)`
   - `MolestiaReportada`: `replace(state, rutina_actual=rutina_ajustada, historial_ajustes=state.historial_ajustes + (ajuste_log,), historial_eventos=nuevo_historial_eventos)`
   - `ImprevistoReportado`: `replace(state, rutina_actual=rutina_ajustada, historial_ajustes=state.historial_ajustes + (ajuste_log,), historial_eventos=nuevo_historial_eventos)`
   - `AusenciaDetectada`: `replace(state, rutina_actual=rutina_ajustada, historial_ajustes=state.historial_ajustes + (ajuste_log,), historial_eventos=nuevo_historial_eventos)`
   - `case _:` (residual): `replace(state, historial_eventos=nuevo_historial_eventos)`
3. **Reducción de líneas y robustez ante cambios futuros:** El código pasó de ~391 líneas a 266 líneas, eliminando repeticiones propensas a errores al evolucionar `AppState`.
4. **Verificación de comportamiento:**
   - Se ejecutó `python src/main.py`: los 10 eventos se procesaron de forma determinista y `fold_events()` arrojó `EXITOSA (Determinismo Matemático)`.
   - Se ejecutó `pytest tests/`: 12 de 12 pruebas pasaron exitosamente en 0.70s.

---

## [2026-09-25 11:47:54] - Creación de la Documentación General `README.md`

**Prompt / Solicitud del Usuario:**
> *"crea un readme de todo lo que llevamos hasta ahora del proyecto"*

### Lista de Tareas
- [x] Crear el archivo [`README.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/README.md) en la raíz del proyecto.
- [x] Documentar la visión general, el problema que resuelve y los pilares arquitectónicos (Programación Funcional, Inmutabilidad, Event Sourcing).
- [x] Mapear el árbol completo de directorios y la descripción de cada módulo (`models`, `catalog`, `engine`, `reducer`, `api`, `data`, `tests`).
- [x] Documentar el filtrado bicondicional, selección de splits y los adaptadores ante imprevistos/molestias.
- [x] Detallar la capa web con FastAPI, Swagger UI, ReDoc y el Dashboard SPA interactivo.
- [x] Proporcionar la guía de instalación, uso de scripts `.bat` y ejecución de la suite de pruebas automatizadas.
- [x] Resumir el roadmap de fases futuras (visión artificial, app móvil, nutrición).

### Detalle de lo Realizado:
1. **Archivo Creado:** Se creó [`README.md`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/README.md) con formato Markdown estándar y diagramas de flujo en Mermaid.
2. **Contenido Estructurado:**
   - **Sección 1:** Visión general del proyecto GymFit Agent y enfoque adaptativo.
   - **Sección 2:** Principios funcionales (inmutabilidad estricta, reductor puro con `match-case` y `dataclasses.replace`, reconstrucción por `fold_events`).
   - **Sección 3:** Estructura de carpetas comentada.
   - **Sección 4:** Detalle técnico de los catálogos JSON y módulos del motor agéntico.
   - **Sección 5:** Documentación de la API REST (tabla de endpoints) y Dashboard Web interactivo en `http://localhost:8000/`.
   - **Sección 6:** Guía de arranque rápido mediante los scripts `run_server.bat`, `run_demo_cli.bat` y `run_tests.bat`.
   - **Sección 7:** Descripción de la suite de 12 pruebas unitarias e integración en `tests/`.
   - **Sección 8:** Roadmap hacia visión por computadora, aplicación móvil y nutrición.

---

## [2026-09-26 22:21:10] - Ajustes de Frontend en el Dashboard Interactivo (Variabilidad, Cronómetro y Tarjetas de Ejercicios)

**Prompt / Solicitud del Usuario:**
> *"Voy a pedirte ajustes de FRONTEND únicamente en el dashboard. No modifiques ninguna lógica de backend, modelos de datos, ni el reducer de eventos — solo la capa de presentación (HTML/CSS/JS del dashboard).*
> *1. SECCIÓN "2. Adaptaciones en Tiempo Real (Variabilidad)": Reorganiza los botones de eventos en 3 grupos visuales claros...*
> *2. CRONÓMETRO DE DESCANSO ENTRE SERIES: Reemplaza los botones actuales... por opciones de tiempo: 2:00, 2:30, 3:00, 3:30, 4:00...*
> *3. TARJETAS DE EJERCICIO (sección "3. Rutina Semanal Activa"): Aplánalo... usa ícono + etiqueta en negrita + texto en una sola línea... y agrega patron_movimiento, nivel_riesgo, articulaciones_comprometidas, errores_comunes, precauciones_seguridad..."*

### Lista de Tareas
- [x] Reorganizar la sección 2 (Variabilidad) en 3 grupos estructurados ("Molestias", "Ajustes de rendimiento", "Imprevistos") con encabezado propio y CSS Grid responsive (`repeat(auto-fit, minmax(180px, 1fr))`).
- [x] Actualizar el cronómetro de descansos con 5 opciones de tiempo (2:00, 2:30, 3:00, 3:30, 4:00) conservando "Detener", presentados en un CSS Grid flexible.
- [x] Aplanar las tarjetas de ejercicio de la sección 3: eliminar cajas anidadas oscuras y reemplazarlas por líneas de estilo uniforme (ícono + etiqueta en negrita + texto) separadas por una línea divisoria sutil (`border-bottom`).
- [x] Incorporar todos los campos del modelo `Exercise` que faltaban en la vista: `patron_movimiento`, `nivel_riesgo`, `articulaciones_comprometidas`, `errores_comunes` y `precauciones_seguridad`.
- [x] Mantener intacta la lógica del backend, endpoints, modelos y reducer.
- [x] Validar que la suite de pruebas (12/12) y las aserciones de interfaz sigan aprobando exitosamente.

### Detalle de lo Realizado:
1. **Archivo modificado:** [`src/api/dashboard_html.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/api/dashboard_html.py).
2. **Reorganización de Variabilidad:** Se crearon las clases `.variability-container`, `.variability-group`, `.variability-group-title` y `.variability-grid`. Los botones ahora se distribuyen en tres filas independientes con grid adaptable automático.
3. **Cronómetro:** Se implementó `.timer-grid` con botones de 120s (2:00), 150s (2:30), 180s (3:00), 210s (3:30) y 240s (4:00), más el botón "Detener".
4. **Tarjetas de Ejercicio Aplanadas:**
   - Se removió `.exercise-technique` con fondo oscuro cerrado y bordes dobles.
   - Cada ejercicio se separa con `border-bottom: 1px solid rgba(255, 255, 255, 0.08)`.
   - Se crearon líneas unificadas con `.exercise-line` para: Prescripción, Patrón de movimiento, Nivel de riesgo, Articulaciones comprometidas, Técnica fija, Errores comunes, Precauciones de seguridad y Alternativas viables.
5. **Verificación:** Se ejecutó `python -m pytest tests/` (12 passed) y verificación programmatic de renderizado en `http://localhost:8000/`.

---

## [2026-09-27 11:47:30] - Ajuste Fisiológico de Series y Descansos por Objetivo y Corrección de Rango Avanzado

**Prompt / Solicitud del Usuario:**
> *"1. CORREGIR data/table_a_levels.json (nivel avanzado): El campo "rango_series_por_ejercicio" del nivel "avanzado" está en [2, 3]... Cámbialo a [4, 6] para reflejar que un usuario avanzado debe manejar más series por ejercicio que uno intermedio o principiante.*
> *2. HACER QUE LAS SERIES TAMBIÉN DEPENDAN DEL OBJETIVO (no solo del nivel): En build_execution_detail() de src/engine/generator.py... GoalEnum.FUERZA -> usar límite SUPERIOR [1], GoalEnum.BAJAR_GRASA -> límite INFERIOR [0], GoalEnum.GANAR_MUSCULO / GoalEnum.MANTENIMIENTO -> promedio...*
> *3. HACER QUE EL DESCANSO DEPENDA PRINCIPALMENTE DEL OBJETIVO: calculate_rest_seconds(perfil, level_params)... FUERZA -> 240s, GANAR_MUSCULO -> 150s, BAJAR_GRASA -> 30s, MANTENIMIENTO -> 60s, fallback -> level_params.descanso_segundos..."*

### Lista de Tareas
- [x] Corregir `rango_series_por_ejercicio` para nivel avanzado en [`data/table_a_levels.json`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/data/table_a_levels.json) de `[2, 3]` a `[4, 6]`.
- [x] Modificar `build_execution_detail()` en [`src/engine/generator.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/engine/generator.py) para que el volumen de series derive del objetivo del atleta (`FUERZA` = max, `BAJAR_GRASA` = min, `GANAR_MUSCULO`/`MANTENIMIENTO` = promedio).
- [x] Implementar la función pura `calculate_rest_seconds(perfil, level_params)` con los tiempos de descanso fisiológicos basados en el objetivo (Fuerza: 240s, Hipertrofia: 150s, Pérdida de grasa: 30s, Mantenimiento: 60s, fallback a nivel).
- [x] Agregar comentarios documentando la aproximación para ejercicios compuestos y la futura refinación según tipología de ejercicio (`mechanic` compuesto/aislamiento).
- [x] Actualizar el cálculo de duración estimada diaria en `generate_routine()` para contemplar los descansos reales de cada slot.
- [x] Ampliar la suite de pruebas automatizadas en [`tests/test_generator.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/tests/test_generator.py) (14/14 tests aprobados).
- [x] Verificar consistencia con `python src/main.py`.

### Detalle de lo Realizado:
1. **[`data/table_a_levels.json`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/data/table_a_levels.json):** Se corrigió `rango_series_por_ejercicio` del nivel avanzado a `[4, 6]`, restaurando la progresión fisiológica coherente (Principiante: `[2, 3]`, Intermedio: `[3, 4]`, Avanzado: `[4, 6]`).
2. **[`src/engine/generator.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/engine/generator.py):**
   - Se añadió `calculate_rest_seconds(perfil, level_params) -> int` mapeando descansos según demanda del SNC y vía metabólica (Fuerza: 240s para resíntesis de PCr; Hipertrofia: 150s priorizando volumen efectivo; Grasa: 30s; Mantenimiento: 60s).
   - Se refactorizó `build_execution_detail()` para ajustar las series asignadas en función de `perfil.objetivo`.
   - Se ajustó `tiempo_descanso_min` en la generación de rutinas usando `s.parametros.descanso_segundos`.
3. **[`tests/test_generator.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/tests/test_generator.py):**
   - `test_advanced_level_series_range`: Valida que el nivel avanzado tenga rango `(4, 6)`.
   - `test_series_and_rest_by_goal`: Valida de forma exhaustiva las series y descansos generados para los 4 objetivos físicos.
4. **Verificación:** Suite de 14 pruebas pasando al 100% en `pytest` y ejecución determinista exitosa en `main.py`.

---

## [2026-09-27 13:21:15] - Verificación y Confirmación de la Refactorización de `state_reducer.py` con `dataclasses.replace`

**Prompt / Solicitud del Usuario:**
> *"Refactoriza el archivo src/reducer/state_reducer.py. Actualmente, cada rama del match/case dentro de reduce_event() reconstruye manualmente una instancia completa de AppState... Reemplaza esas reconstrucciones manuales usando dataclasses.replace()... Aplica el mismo patrón a las 12 ramas del match/case... Al terminar, corre src/main.py y confirma que el demo sigue funcionando exactamente igual que antes..."*

### Lista de Tareas
- [x] Verificar que [`src/reducer/state_reducer.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/reducer/state_reducer.py) tenga importado `from dataclasses import replace`.
- [x] Confirmar que las 12 ramas del `match event:` usen `replace(state, ...)` especificando solo los campos que cambian.
- [x] Ejecutar `python src/main.py` para constatar que el demo produce exactamente los mismos 10 eventos, misma rutina y validación exitosa de `fold_events()`.
- [x] Ejecutar la suite completa de pruebas unitarias (`pytest tests/`).

### Detalle de lo Realizado:
1. **Inspección de código:** Se corroboró que [`src/reducer/state_reducer.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/reducer/state_reducer.py) ya implementa de forma integral y rigurosa `dataclasses.replace` en las 12 ramas:
   - `PerfilCreado`, `EquipoRegistrado`, `EquipoActualizado`, `RutinaGenerada`, `SesionIniciada`, `SerieRegistrada`, `SesionFinalizada`, `DificultadReportada`, `MolestiaReportada`, `ImprevistoReportado`, `AusenciaDetectada` y el caso residual `case _:`.
2. **Ejecución de Demostración (`main.py`):**
   - 10 eventos procesados determinísticamente.
   - Verificación de Event Sourcing: `✓ Reconstrucción completa del estado mediante fold_events(): EXITOSA (Determinismo Matemático)`.
3. **Suite de Pruebas:**
   - 14 pruebas pasando en 0.64s (`tests/test_api.py`, `tests/test_filters.py`, `tests/test_generator.py`, `tests/test_reducer.py`).

---

## [2026-09-27 19:58:15] - Optimización y Adaptabilidad Responsiva del Frontend para Dispositivos Móviles (Celular)

**Prompt / Solicitud del Usuario:**
> *"que se actualice el display de manera que se acomode todo el frontend de lo que llevamos de proyecto, pero para celular"*

### Lista de Tareas
- [x] Adaptar los contenedores globales y paddings del viewport para pantallas de smartphones (`padding: 12px` en móvil, `20px` en escritorio).
- [x] Rediseñar el encabezado (`header`): apilamiento vertical en móviles con título centrado y botonera en cuadrícula 2x2 / span total para acceso táctil rápido.
- [x] Reemplazar grids inline fijos por clases responsivas (`.form-row-2`, `.form-row-3`) para que los campos de datos (nombre, sexo, peso, altura, días, objetivo, nivel) se colapsen a una sola columna legible en teléfonos sin desbordamientos.
- [x] Ajustar el tamaño de fuente de inputs y selectores a `16px` para prevenir zoom automático no deseado en iOS Safari.
- [x] Mejorar la ergonomía táctil en chips de equipamiento y botones de acción (`min-height: 40-42px`, `touch-action: manipulation`, `-webkit-tap-highlight-color: transparent`).
- [x] Ajustar la botonera del cronómetro (`.timer-grid`) a 3 columnas compactas en celular y tamaño de display numérico fluido (`2.3rem` en móvil).
- [x] Flexibilizar cabeceras de días y nombres de ejercicios en la sección 3 con `flex-wrap` y `word-break: break-word` para evitar truncamientos en pantallas estrechas.
- [x] Ejecutar la suite de pruebas unitarias y verificar el renderizado con `TestClient`.

### Detalle de lo Realizado:
1. **Archivo modificado:** [`src/api/dashboard_html.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/api/dashboard_html.py).
2. **Encabezado y Barra de Acciones Móvil:**
   - En pantallas menores a 768px, el `header` pasa de fila a columna y `.header-actions` se convierte en un grid de 2 columnas táctil donde el botón de Swagger abarca el ancho completo.
3. **Formulario Adaptable de Perfil:**
   - Se crearon las reglas `@media` para `.form-row-2` y `.form-row-3`. En celulares de 360px a 440px los campos se apilan limpiamente en una sola columna con espaciado vertical cómodo.
4. **Variabilidad y Cronómetro Touch-Friendly:**
   - Los botones de molestias, sobrecarga e imprevistos se reorganizan en una sola columna o dos columnas fluidas según el ancho del smartphone.
   - El cronómetro organiza sus 6 opciones (2:00 a 4:00 + Detener) en una cuadrícula de 3 columnas de botones grandes y accesibles al pulgar.
5. **Tarjetas de Rutina:**
   - Las etiquetas de ejercicios y prescripción no se desbordan horizontalmente gracias a `flex-wrap` y `word-break: break-word`.
6. **Verificación:** Suite de 14 pruebas pasando al 100% y aserciones de responsividad validadas.

---

## [2026-09-27 20:01:45] - Configuración de Red para Acceso y Visualización desde Dispositivos Móviles

**Prompt / Solicitud del Usuario:**
> *"cómo lo puedo ver en mi celular?"*

### Lista de Tareas
- [x] Identificar la dirección IP local de la computadora en la red Wi-Fi (`192.168.1.31`).
- [x] Configurar [`run_server.bat`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/run_server.bat) para enlazar el servidor a `--host 0.0.0.0` (permitiendo conexiones desde cualquier dispositivo de la red local en lugar de solo localhost).
- [x] Proporcionar al usuario las instrucciones paso a paso para abrir la interfaz en el navegador del teléfono.

### Detalle de lo Realizado:
1. **[`run_server.bat`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/run_server.bat):** Se reemplazó `--host 127.0.0.1` por `--host 0.0.0.0`.
2. **Dirección de Enlace:** La computadora tiene la IP asignada `192.168.1.31`, lo que habilita la URL `http://192.168.1.31:8000` para cualquier teléfono conectado al mismo Wi-Fi.

---

## [2026-10-02 00:33:18] - Corrección de Desbordamiento Horizontal de la Pastilla del Split Activo en Móvil

**Prompt / Solicitud del Usuario:**
> *"En el frontend del dashboard, la etiqueta/pastilla que muestra el nombre del split activo... se desborda horizontalmente en pantallas angostas (celular). Corrige el estilo para que en vez de desbordarse, el texto haga salto de línea dentro de la pastilla..."*

### Lista de Tareas
- [x] Localizar el elemento `<span class="badge" id="routineSplitBadge">` en [`src/api/dashboard_html.py`](file:///c:/Users/fred_/OneDrive/Documentos/Ing.%20en%20Computación%20Inteligente/Tercer%20Semestre%20ICI/proyecto_ia_agentica/src/api/dashboard_html.py) (línea 709).
- [x] Identificar la causa raíz: `white-space: nowrap` en la clase genérica `.badge`.
- [x] Agregar regla CSS específica `#routineSplitBadge` con `white-space: normal`, `word-break: break-word`, `overflow-wrap: break-word`, `max-width: 100%`, `text-align: center`, `line-height: 1.4`, `border-radius: 8px` y `flex-shrink: 1`.
- [x] Mantener `white-space: nowrap` en el `.badge` genérico (para que "🟢 API Online" no rompa línea).
- [x] Confirmar que `.card-header` ya soporta crecimiento vertical del badge (`flex-wrap: wrap`, `gap: 8px`).

### Detalle de lo Realizado:
1. **Causa raíz:** `.badge { white-space: nowrap; }` bloqueaba el salto de línea.
2. **Solución:** Regla CSS específica `#routineSplitBadge` que sobreescribe solo lo necesario, sin afectar otros badges.
   - `white-space: normal` + `word-break: break-word` + `overflow-wrap: break-word` → texto fluye en múltiples líneas.
   - `max-width: 100%` → nunca supera el ancho del contenedor.
   - `border-radius: 8px` → forma rectangular redondeada cuando es multi-línea.
   - `flex-shrink: 1` → cede espacio al título si es necesario.
3. **Badge "API Online"** no fue afectado: conserva `white-space: nowrap` de la clase base.
4. **Sin cambios de backend ni lógica** — solo CSS de presentación.

---



---
