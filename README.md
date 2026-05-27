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
