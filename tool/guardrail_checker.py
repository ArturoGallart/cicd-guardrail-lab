#!/usr/bin/env python3
"""
guardrail_checker.py
Detector determinista de 3 patrones de riesgo clásicos en workflows de GitHub Actions.
No usa IA: las reglas están encapsuladas en código para que nunca dependan
de que un modelo "se acuerde" de revisarlas.
"""
import re
import sys
import json


def _line_number(text, match_start):
    """Devuelve el número de línea (1-indexado) donde empieza el match."""
    return text.count("\n", 0, match_start) + 1


def check_mutable_action_refs(workflow_text):
    findings = []
    for match in re.finditer(r'uses:\s*([^\s@]+)@([^\s]+)', workflow_text):
        action, ref = match.group(1), match.group(2)
        if not re.fullmatch(r'[0-9a-f]{40}', ref):
            findings.append({
                "rule": "mutable-action-ref",
                "severity": "medium",
                "line": _line_number(workflow_text, match.start()),
                "detail": f"'{action}' referenciado por '{ref}' en vez de un hash fijo.",
                "suggestion": f"Fija '{action}' a un commit SHA completo en vez de un tag.",
            })
    return findings


def check_latest_tag_usage(workflow_text):
    """
    Busca 'latest' como palabra suelta, excluyendo:
    - casos pegados con un guion justo antes (p. ej. 'ubuntu-latest'), que son
      nombres de runner/imagen, no una versión de herramienta sin fijar.
    - líneas de comentario YAML completas (cuyo primer carácter no blanco es '#'),
      para no generar falsos positivos por texto explicativo.
    Nota: no cubre comentarios al final de una línea de código (ej. "run: algo # latest"),
    solo líneas que son comentario desde su inicio. Suficiente para el alcance de este lab.
    """
    for line_num, line in enumerate(workflow_text.splitlines(), start=1):
        if line.lstrip().startswith('#'):
            continue
        match = re.search(r'(?<!-)\blatest\b', line)
        if match:
            return [{
                "rule": "latest-tag-usage",
                "severity": "medium",
                "line": line_num,
                "detail": "Se detectó el uso de 'latest' para instalar o referenciar una herramienta.",
                "suggestion": "Fija una versión explícita y conocida en vez de 'latest'.",
            }]
    return []


def check_shell_injection_risk(workflow_text):
    """
    Ubica cada interpolación de 'github.event.inputs.*' y reporta su línea real
    solo si el 'run:' más cercano hacia atrás está más cerca que el límite del
    step anterior ('- name:' / '- uses:') — es decir, si la interpolación cae
    dentro de un bloque de shell, no solo en algún punto posterior del archivo.
    """
    input_pattern = re.compile(r'\$\{\{\s*github\.event\.inputs\.[\w.]+\s*\}\}')
    run_pattern = re.compile(r'^\s*run:', re.MULTILINE)
    step_boundary_pattern = re.compile(r'^\s*-\s+(name|uses):', re.MULTILINE)

    for m in input_pattern.finditer(workflow_text):
        pos = m.start()

        last_run = None
        for rm in run_pattern.finditer(workflow_text, 0, pos):
            last_run = rm

        last_boundary = None
        for bm in step_boundary_pattern.finditer(workflow_text, 0, pos):
            last_boundary = bm

        if last_run and (not last_boundary or last_run.start() > last_boundary.start()):
            return [{
                "rule": "shell-injection-risk",
                "severity": "high",
                "line": _line_number(workflow_text, pos),
                "detail": "Una entrada de usuario del workflow se interpola directamente en un script de shell.",
                "suggestion": "Pasa la entrada como variable de entorno validada, no interpolada directamente en 'run'.",
            }]
    return []


# --- Punto de extensión para el Paso 3 del laboratorio ---
# Agrega aquí nuevas funciones check_*() siguiendo el mismo patrón:
# reciben el texto del workflow y devuelven una lista de hallazgos.
# No agregues lógica de detección nueva en el SKILL.md — siempre aquí.


def main(path):
    with open(path, "r") as f:
        text = f.read()

    findings = (
        check_mutable_action_refs(text)
        + check_latest_tag_usage(text)
        + check_shell_injection_risk(text)
    )

    print(json.dumps({"file": path, "findings": findings}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python guardrail_checker.py <ruta-al-workflow.yml>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
