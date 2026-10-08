# Checklist final — Guardrails para skills de IA en producción

Antes de confiar un skill de IA a un flujo de producción, verifica:

- [ ] El contrato de entrada/salida está documentado explícitamente (qué recibe, qué produce, en qué formato).
- [ ] El skill nunca inventa valores reales — usa placeholders y registra decisiones pendientes con severidad.
- [ ] Cada hallazgo de análisis está etiquetado con fuente, evidencia y nivel de confianza.
- [ ] La generación y la validación son pasos separados, y la validación ejecuta herramientas reales, no solo revisa el texto generado.
- [ ] Se corrió al menos un piloto real (no solo pruebas sintéticas) antes de generalizar el skill.
- [ ] Se auditó el resultado del piloto buscando específicamente fallas silenciosas (todo en verde, resultado real desalineado), no solo errores explícitos.
- [ ] Las versiones de herramientas externas invocadas están fijadas y verificadas antes de confiar en sus resultados.
- [ ] Existe una checklist de seguridad específica del dominio que se ejecuta antes de dar por cerrada una corrida.
- [ ] Los errores de razonamiento repetibles detectados se resolvieron encapsulando la lógica en código determinista, no solo ajustando el prompt.

---
*De la charla "Claude Skills en AWS: implementando IA en tu flujo de DevOps".*
