# Reproducibility

## Todo resultado debe poder reconstruirse
Registrar:
- git commit/release;
- dataset snapshot id + hash;
- scenario version;
- policy version;
- BKT parameter set/version;
- metric implementation version;
- random seed cuando aplique;
- timezone y calendario usados;
- experiment protocol version.

## Datos
No depender durante el análisis final de una API que pueda cambiar. Descargar/preparar snapshots con metadatos de origen y licencia.

## Experimentos
Exportar un paquete de análisis desidentificado con:
- schema;
- datos necesarios;
- script/notebook reproducible;
- README de ejecución;
- tabla de exclusiones.

## Determinismo
El sistema no necesita ser 100 % determinista en UI, pero las decisiones experimentales deben poder reproducirse con el registro de seed/policy/candidatos.
