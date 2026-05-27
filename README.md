# Restaurant API Security Project

Este proyecto forma parte de la asignatura Optativa (Periodo 2610) y se enfoca en el análisis, explotación y mitigación de vulnerabilidades en una API de restaurante.
(componente:autenticacion)
## Estructura del Repositorio

- `vulnerable-app/`: Repositorio original(Damn Vulnerable Restaurant API Game).
- `member-1-hashing/`: Análisis y mitigación de Hashing débil de contraseñas.
- `member-2-jwt/`: Análisis y mitigación de JWT inseguro.
- `member-3-rate-limit/`: Análisis y mitigación de falta de Rate Limiting.
- `member-4-authz/`: Análisis y mitigación de Escalada de privilegios.
- `docs/`: evidencia de cumplimiento de trabajo y reflexiones

## Objetivo
Identificar vulnerabilidades críticas basadas en el OWASP API Security Top 10 (2023), explotarlas éticamente y proponer mitigaciones robustas.

<<<<
<<< member-3-rate-limit


# Restaurant API Security Project

## Integrante

Rodrigo Manuel Alfaro Giraldo

## Vulnerabilidad Analizada

OWASP API4:2023 — Unrestricted Resource Consumption

## Descripción

Este proyecto corresponde al análisis, explotación y mitigación de vulnerabilidades en una API vulnerable llamada Damn Vulnerable RESTaurant API.

La vulnerabilidad seleccionada fue la ausencia de mecanismos de Rate Limiting sobre el endpoint de autenticación `/token`.

La ausencia de limitación de solicitudes permitía ataques automatizados, fuerza bruta y consumo excesivo de recursos.

---

# Tecnologías utilizadas

* Python 3.10
* FastAPI
* Docker
* PostgreSQL
* SlowAPI
* Swagger/OpenAPI
* PowerShell

---

# Vulnerabilidad identificada

Endpoint vulnerable:

```python
POST /token
```

Problema identificado:

* solicitudes ilimitadas
* ausencia de Rate Limiting
* posibilidad de ataques automatizados

OWASP relacionado:

```txt
API4:2023 — Unrestricted Resource Consumption
```

---

# Explotación

Se realizaron múltiples solicitudes automatizadas utilizando PowerShell.

La API aceptaba solicitudes ilimitadas sin bloqueos ni respuestas HTTP 429.

---

# Mitigación implementada

Se implementó Rate Limiting utilizando SlowAPI.

Configuración aplicada:

```python
@limiter.limit("5/minute")
```

La mitigación permitió:

* limitar solicitudes por IP
* bloquear automatización excesiva
* reducir riesgo de fuerza bruta

---

# Validación

Después de implementar la mitigación:

* las primeras solicitudes fueron exitosas
* las solicitudes posteriores fueron bloqueadas
* la API respondió:

```txt
Rate limit exceeded: 5 per 1 minute
```

---

# Reflexión ética

La ausencia de controles básicos de seguridad puede comprometer la disponibilidad y estabilidad de un sistema.

El ingeniero de software tiene la responsabilidad de implementar mecanismos de protección adecuados y desarrollar aplicaciones seguras desde las primeras etapas del desarrollo.

---

## Guía para el Equipo (Colaboración)

Para trabajar de forma organizada, cada integrante tiene su propia rama, si sale error es porque hacen push a main y no tienen permiso pa eso. Sigan estos pasos:

### 1. Clonar el repositorio
Abran una terminal y ejecuten:
```bash
git clone https://github.com/realprodigium/restaurant-api-security.git
cd restaurant-api-security
```

### 2. Cambiar a su rama asignada
Busquen su número de integrante y ejecuten el comando correspondiente:
- **Integrante 1:** `git checkout member-1-hashing`
- **Integrante 2:** `git checkout member-2-jwt`
- **Integrante 3:** `git checkout member-3-rate-limit`
- **Integrante 4:** `git checkout member-4-authz`

### 3. Guardar sus cambios
Cuando terminen de trabajar en su carpeta, suban los cambios a su rama:
```bash
git add .
git commit -m "Descripción de lo que hiciste"
git push origin NOMBRE_DE_TU_RAMA
```

### 4. Integración final
ya solo queda que el owner del repo envíe a main
>>> main
