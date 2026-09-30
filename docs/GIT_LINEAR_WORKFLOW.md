# Git + Linear Workflow

## Fuente de verdad
- Linear: trabajo operativo, estado, prioridad y bloqueos.
- GitHub: código, ramas, Pull Requests, revisión, CI y releases.
- `docs/`: decisiones durables, científicas y de arquitectura.

## Kanban
`Backlog → Ready → In Progress → Review → Validation → Done`

Estado adicional: `Blocked`.

## Issue
Formato recomendado: `II-###` en el título o identificador equivalente de Linear, con criterios de aceptación verificables.

Evitar issues gigantes como “hacer backend”. Preferir vertical slices o cambios científicos/técnicos acotados.

## GitFlow simplificado
```text
main
 └─ develop
     ├─ feature/II-123-scenario-lock
     ├─ fix/II-124-brier-rounding
     └─ docs/II-125-protocol-freeze
```

## Pull Request
Debe incluir:
- issue vinculada;
- qué cambió;
- tests ejecutados;
- impacto científico si existe;
- migraciones si corresponden;
- capturas cuando cambie la UI;
- riesgos o deuda técnica conocida.

## Merge
Todo merge a ramas protegidas requiere revisión humana y CI en verde.
