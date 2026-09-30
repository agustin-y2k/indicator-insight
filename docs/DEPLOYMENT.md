# Deployment

## Objetivo
Demo estable en servidor propio, sin exponer puertos del router directamente.

```text
Internet
 ↓
Cloudflare
 ↓
Cloudflare Tunnel
 ↓
Docker host
 ├─ frontend
 ├─ backend
 └─ postgres
```

## Entornos
- dev: local;
- staging: integración/datos sintéticos;
- production/demo: release etiquetada.

No ejecutar el experimento principal contra una versión que cambia continuamente.

## Backups
- dump PostgreSQL programado;
- snapshots de datasets fuera del volumen efímero;
- prueba periódica de restore.

## Secrets
Tunnel token, DB passwords y cualquier credencial sólo por environment/secret file no versionado.
