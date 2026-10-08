---
name: cicd-guardrail-review
description: >
  Revisa un workflow de CI/CD invocando el detector determinista guardrail_checker.py
  y traduce sus hallazgos en un comentario de PR legible, categorizado por severidad,
  con sugerencias de corrección accionables. Úsalo cuando el usuario pida revisar
  un workflow de GitHub Actions antes de abrir o mergear un PR.
---

# Instrucciones

1. Identifica la ruta del archivo de workflow que el usuario quiere revisar.
2. Ejecuta: `python tool/guardrail_checker.py <ruta-del-workflow>`
   - NO reimplementes la lógica de detección en este prompt. La fuente de verdad
     de qué es o no un hallazgo es siempre la salida de ese script.
3. Toma el JSON de salida y redáctalo como un comentario de revisión de PR:
   - Agrupa los hallazgos por severidad (alta primero).
   - Para cada hallazgo, explica en una frase por qué importa (no solo repitas el
     campo "detail" tal cual) y presenta la sugerencia como un cambio concreto.
   - Si no hay hallazgos, dilo explícitamente — no inventes advertencias.
4. Si el usuario pide agregar una nueva regla de detección, NO la agregues como
   una instrucción nueva en este archivo — edita `tool/guardrail_checker.py` para
   añadir una función de chequeo determinista nueva. Este skill solo interpreta
   resultados, nunca decide por su cuenta qué es una vulnerabilidad.
