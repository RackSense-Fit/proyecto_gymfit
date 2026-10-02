# Propuesta de Proyecto — Agente de Inteligencia Artificial Agéntica

## 1. Nombre provisional
**GymFit Agent** (nombre provisional, sujeto a cambios en fases posteriores).

## 2. Problema o necesidad
La mayoría de las rutinas de entrenamiento que se encuentran en aplicaciones, videos o redes sociales asumen un gimnasio "ideal" con equipo estándar, pero en la realidad **cada gimnasio tiene máquinas, pesos y equipo distintos**, y muchas veces le falta justo el aparato que la rutina "genérica" requiere. Esto obliga al usuario a improvisar, adaptar por su cuenta (a veces mal) o simplemente sentir que la rutina no le sirve para el lugar donde realmente entrena. Además, esa rutina suele ser estática: no considera que el usuario puede tener un mal día, menos tiempo del planeado, molestias físicas o que su gimnasio cambie de equipo con el tiempo. El problema real que se busca resolver es que **la persona reciba una rutina construida específicamente con el equipo que tiene disponible en su propio gimnasio, y que esa rutina pueda ajustarse cuando las condiciones cambien**, en lugar de recibir un plan genérico y rígido.

## 3. Usuario
El sistema está dirigido a personas que entrenan por su cuenta y no cuentan con un entrenador personal que diseñe su rutina a la medida del equipo real disponible: estudiantes, jóvenes profesionistas, personas que inician en el gimnasio sin experiencia previa, y también quienes ya entrenan pero cambian de gimnasio con frecuencia (viajes, mudanzas, gimnasios de trabajo/escuela) y necesitan adaptar su rutina al nuevo lugar.

## 4. Funcionamiento general
El usuario toma fotos del equipo disponible en su gimnasio (bancos, mancuernas, máquinas, barras, etc.), acompañadas de una breve especificación cuando sea necesario (por ejemplo, rango de pesos disponibles o el nombre/función de la máquina si no es evidente en la foto). Junto con esto, el usuario proporciona su perfil: sexo, peso, altura, objetivo (bajar de peso, ganar masa muscular, mantenimiento, fuerza, etc.), nivel de experiencia (si ya ha entrenado antes o es principiante) y los días disponibles a la semana para entrenar. Con toda esta información, el agente **analiza** qué ejercicios son posibles con el equipo real identificado, **decide** cómo distribuir esos ejercicios en un split semanal acorde al nivel, objetivo y días disponibles del usuario, y **actúa** generando la rutina correspondiente.

Durante cada sesión de entrenamiento, el usuario puede **registrar su desempeño real**: peso utilizado, repeticiones, series completadas y tiempo de descanso entre series (apoyado por un cronómetro integrado cuyo tiempo queda grabado como parte del historial de esa sesión). Este registro se organiza en un **calendario de entrenamiento**, que permite ver de un vistazo qué días se entrenó durante el mes y llevar un conteo de sesiones completadas, sirviendo también como base de datos histórica del progreso del usuario.

El agente no entrega una rutina fija: si el usuario reporta dificultades (un ejercicio le resulta muy pesado, muy fácil, le genera molestia en alguna zona, cambia de gimnasio y sube fotos de un equipo distinto) o **variabilidad de su día a día** (no pudo asistir un día y necesita reformular la rutina restante de la semana, durmió mal la noche anterior, tiene poco tiempo disponible, etc.), el sistema **reanaliza y ajusta la rutina** en consecuencia, en lugar de mantener un plan estático o simplemente marcar el día como "incumplido".

## 5. Responsabilidades del agente
1. **Analizar el equipo disponible** a partir de las fotos y especificaciones proporcionadas por el usuario, determinando qué ejercicios son viables con esos recursos.
2. **Decidir y generar una rutina personalizada**, combinando el equipo disponible con el perfil del usuario (objetivo, nivel, días disponibles) para construir un split de entrenamiento adecuado.
3. **Ajustar la rutina de forma continua** ante cambios reportados por el usuario: dificultad excesiva o insuficiente en un ejercicio, molestias físicas, cambio de gimnasio/equipo, o variaciones en la disponibilidad de días, generando una versión actualizada del plan sin necesidad de reiniciar el proceso desde cero.
4. **Reaccionar a la variabilidad del día a día del usuario**, como no poder asistir un día programado y necesitar reformular el resto de la semana, mala calidad de sueño, poco tiempo disponible u otros imprevistos, decidiendo cómo reorganizar la rutina restante sin penalizar el progreso general del usuario.

## 6. Información necesaria
El sistema deberá recibir, consultar, transformar o almacenar:
- **Fotos y especificaciones del equipo:** imágenes del gimnasio del usuario y datos adicionales sobre el equipo cuando la foto no sea suficiente (rango de pesos, nombre de la máquina, etc.).
- **Datos de perfil:** sexo, peso, altura, objetivo y nivel de experiencia del usuario.
- **Disponibilidad:** número de días a la semana que el usuario puede entrenar.
- **Retroalimentación del usuario:** dificultad percibida por ejercicio, molestias reportadas, cambios de equipo o de gimnasio.
- **Registro de sesión:** peso utilizado, repeticiones, series completadas y tiempos de descanso (capturados mediante un cronómetro) para cada ejercicio realizado.
- **Calendario de entrenamiento:** fechas en las que el usuario entrenó, permitiendo un conteo de sesiones completadas por mes.
- **Señales de variabilidad diaria:** ausencias no planeadas, calidad de sueño reportada, tiempo disponible ese día u otros imprevistos que afecten la sesión.
- **Historial de la rutina:** ejercicios asignados previamente y ajustes realizados, para no repetir errores anteriores al generar nuevas versiones del plan.

## 7. Resultado esperado
El usuario recibirá:
- Una rutina de entrenamiento semanal (split) construida específicamente con el equipo real disponible en su gimnasio.
- Ejercicios agrupados por día según su objetivo, nivel y días disponibles a la semana.
- Ajustes a la rutina cuando reporte dificultades, molestias, cambios en su equipo disponible, o variabilidad de su día a día (ausencias, mal descanso, poco tiempo), sin tener que empezar de nuevo el proceso.
- Un registro por sesión de los pesos, repeticiones, series y tiempos de descanso utilizados, con un cronómetro que queda grabado como parte del historial de ese entrenamiento.
- Un calendario visual con el conteo de días entrenados por mes, que le permita ver su constancia a lo largo del tiempo.
- Con el tiempo, un plan cada vez más afinado a su progreso y a las condiciones reales de su entrenamiento.

Es importante señalar que el agente **apoya el diseño de la rutina, no sustituye la valoración de un entrenador certificado o profesional de la salud**, especialmente en casos de lesión o molestia física persistente, donde se recomendará al usuario acudir con un especialista.

## 8. Valor de la propuesta
A diferencia de las rutinas genéricas que asumen un gimnasio "tipo" con equipo estándar, este agente **construye la rutina a partir del equipo real que el usuario tiene disponible**, evitando la frustración de recibir ejercicios que no se pueden realizar en su lugar de entrenamiento. Además, mantiene el mismo principio de adaptabilidad que hace sostenible este tipo de proyectos a largo plazo: la rutina no es un documento fijo, sino un plan que **se ajusta cuando la realidad del usuario cambia** (dificultad, molestias, cambio de gimnasio), en lugar de exigir que el usuario se adapte a un plan rígido o lo abandone.

Para esta primera etapa, el proyecto se enfoca exclusivamente en el reconocimiento de equipo y generación/ajuste de rutinas de entrenamiento. Como evolución futura, una vez validado este componente, se contempla **integrar el enfoque nutricional trabajado previamente** (registro de comidas, balance calórico y adaptación a imprevistos de la vida diaria), de manera que ambos módulos —entrenamiento y alimentación— converjan en una sola aplicación o plataforma más completa, manteniendo en ambos casos el mismo principio de adaptación continua a la realidad del usuario.
