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


def check_mutable_action_refs(workflow_text):
    findings = []
    for match in re.finditer(r'uses:\s*([^\s@]+)@([^\s]+)', workflow_text):
        action, ref = match.group(1), match.group(2)
        if not re.fullmatch(r'[0-9a-f]{40}', ref):  # no es un hash SHA completo
            findings.append({
                "rule": "mutable-action-ref",
                "severity": "medium",
                "detail": f"'{action}' referenciado por '{ref}' en vez de un hash fijo.",
                "suggestion": f"Fija '{action}' a un commit SHA completo en vez de un tag.",
            })
    return findings


def check_latest_tag_usage(workflow_text):
    findings = []
    if re.search(r'\blatest\b', workflow_text):
        findings.append({
            "rule": "latest-tag-usage",
            "severity": "medium",
            "detail": "Se detectó el uso de 'latest' para instalar o referenciar una herramienta.",
            "suggestion": "Fija una versión explícita y conocida en vez de 'latest'.",
        })
    return findings


def check_shell_injection_risk(workflow_text):
    findings = []
    # Heurística simple: ${{ github.event.inputs.* }} usado dentro de un bloque 'run'
    if re.search(r'run:\s*\|?[\s\S]*?\$\{\{\s*github\.event\.inputs', workflow_text):
        findings.append({
            "rule": "shell-injection-risk",
            "severity": "high",
            "detail": "Una entrada de usuario del workflow se interpola directamente en un script de shell.",
            "suggestion": "Pasa la entrada como variable de entorno validada, no interpolada directamente en 'run'.",
        })
    return findings


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
