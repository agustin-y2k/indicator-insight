# Frontend

## Stack
React + TypeScript.

## Principios UX
La UI debe evitar patrones de trading gamificado que incentiven volumen o euforia.

No incluir por defecto:
- rankings por rentabilidad;
- confetti por acertar;
- rachas de ganancias;
- notificaciones de “oportunidad”; 
- lenguaje de compra/venta como recomendación.

## Flujo principal
1. contexto/evidencia del escenario;
2. ítem conceptual cuando corresponda;
3. pronóstico probabilístico mediante control accesible 0–100 %;
4. confirmación/lock del intento;
5. resolución y feedback;
6. explicación de aprendizaje (separando concepto, outcome y probabilidad);
7. siguiente escenario.

## Visualizaciones
- evolución de dominio por competencia;
- Brier por bloque/sesión con N visible;
- reliability diagram sólo cuando haya muestras suficientes;
- historial auditable de intentos;
- explicación simplificada de por qué se seleccionó el siguiente escenario.

## Testing
Playwright cubre el flujo científico end-to-end, no sólo navegación.
