# CI/CD Guardrail Checker — Laboratorio

Este laboratorio reproduce una lección de la charla **"Claude Skills en AWS: implementando IA en tu flujo de DevOps"**: un LLM puede generar CI/CD con vulnerabilidades clásicas, y la forma correcta de atraparlas es una herramienta determinista + un skill que la envuelve — no "un mejor prompt".

Todo el contenido de este repo es sintético (sin nombres de cliente, repos reales ni arquitectura propietaria).

## Requisitos

- Python 3.9+
- (Opcional, para el Paso 2) Claude Code u otra herramienta de Claude Skills

## Estructura

```
cicd-guardrail-lab/
├── README.md
├── examples/
│   └── vulnerable-workflow.yml        # pipeline sintético con 3 problemas de seguridad
├── tool/
│   └── guardrail_checker.py           # detector determinista
└── .claude/
    └── skills/
        └── cicd-guardrail-review/
            └── SKILL.md                # skill que envuelve al checker
```

## ¿Por qué está separado así?

El checker (`tool/guardrail_checker.py`) es código normal: detecta los 3 patrones de riesgo con reglas explícitas, sin IA de por medio. El skill (`cicd-guardrail-review`) **no reimplementa esa detección** — solo invoca el script y traduce su salida en un comentario de PR legible. Esta separación es intencional: el skill de IA no decide qué es una vulnerabilidad, eso ya lo decidió el código determinista. El skill solo comunica y contextualiza el resultado.

## Pasos

### Paso 1 — Ver el problema en crudo

```bash
python tool/guardrail_checker.py examples/vulnerable-workflow.yml
```

Deberías ver 3 hallazgos en JSON: una referencia de acción mutable, el uso de `latest`, y un riesgo de inyección de shell.

### Paso 2 — Ver el valor del skill

Con Claude Code (u otra herramienta de skills disponible), invoca el skill `cicd-guardrail-review` sobre el mismo archivo. Compara: ahora deberías obtener un comentario de PR redactado y priorizado, no solo JSON crudo.

### Paso 3 — El reto: agrega una 4ª regla

Elige uno:
- Detectar `permissions: write-all` (permisos de workflow demasiado amplios).
- Detectar un secreto referenciado sin pasar por `env:` explícito.

Instrucciones:
1. Escribe la nueva función de chequeo determinista en `tool/guardrail_checker.py` — **no** la agregues como instrucción en el `SKILL.md`.
2. Vuelve a correr el skill y confirma que el comentario de PR ahora incluye el nuevo hallazgo, sin haber tocado `SKILL.md`.

Esto demuestra que extender la cobertura de seguridad es un cambio de código determinista, no un cambio de prompt.

### Paso 4 (opcional, stretch goal) — Desplegarlo en AWS

Empaqueta `guardrail_checker.py` como una función Lambda simple, invocada por un paso de GitHub Actions en cada PR, usando créditos AWS.

## Más contexto

Ver la guía completa: `guia-diseno-endurecimiento-skills-ia.md` (de la misma charla) para los principios generales de diseño y endurecimiento de skills de IA.
