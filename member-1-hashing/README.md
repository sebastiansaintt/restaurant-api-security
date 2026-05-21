# Módulo 1: Seguridad en Autenticación y Hashing

**Integrante:** Sebastian (Member 1)  
**OWASP Cubierto:** API2:2023 (Broken Authentication), A02:2021 (Cryptographic Failures), A07:2021 (Auth Failures)

---

## 🎯 El Problema (Vulnerabilidad)
La aplicación original carecía de defensas robustas en la capa de autenticación. Utilizar algoritmos de hashing rápidos o configuraciones por defecto permite a los atacantes usar fuerza bruta o GPUs para crackear contraseñas masivamente. Además, no había validación de fuerza de contraseña ni protección contra ataques de tiempo (Timing Attacks), lo que facilitaba el robo de cuentas.

*   **Impacto:** Riesgo de robo masivo de credenciales en caso de fuga de la base de datos (Data Breach).
*   **Ética:** Como ingenieros, debemos proteger la identidad del usuario desde el diseño ("Security by Design"). Dejar puertas abiertas por negligencia o ignorar los estándares de la industria (NIST/OWASP) compromete la confianza de los clientes.

---

## 📸 Evidencia del Antes (Vulnerabilidad Activa)

> **[Inserta aquí la imagen 1: El código original débil en utils.py]**
> *Se observa la falta de validaciones y el uso de configuraciones criptográficas por defecto.*

> **[Inserta aquí la imagen 2: La base de datos original]**
> *Las contraseñas almacenadas no tienen el factor de protección necesario contra hardware moderno.*

---

## 🛡️ La Solución (Hardening y Mitigación)
Implementé un esquema de protección multicapa:

1.  **Políticas de Contraseñas (A07:2021):** Se agregó Regex para exigir mínimo 8 caracteres, mayúsculas, minúsculas, números y símbolos.
2.  **Hardening Criptográfico (A02:2021):** Migración a **Argon2id** (Estándar de Oro) con parámetros "Memory-Hard" explícitos (`memory_cost=64MB`, `time_cost=3`). Esto frena en seco el cracking por GPU.
3.  **Defensa Anti-Timing Attacks:** Si un usuario no existe, el servidor calcula un hash "dummy" para que la respuesta tarde lo mismo, evitando que el atacante "adivine" usuarios midiendo milisegundos.
4.  **Tarpitting:** Cada intento fallido añade un retraso de 0.5s, desincentivando la fuerza bruta.

---

## 📸 Evidencia del Después (Mitigación Activa)

> **[Inserta aquí la imagen 3: Swagger - Fallo al crear contraseña débil]**
> *La API rechaza la contraseña "password123" por no cumplir la política (Error 400).*

> **[Inserta aquí la imagen 4: Base de Datos - Hash Argon2id]**
> *El nuevo hash es visiblemente más complejo y contiene los parámetros de costo configurados (`$argon2id$v=19$m=65536,t=3,p=4...`).*

> **[Inserta aquí la imagen 5: Tiempos de Respuesta Constantes]**
> *Terminal mostrando que un login fallido (usuario inventado vs usuario real con mala clave) toma exactamente el mismo tiempo, mitigando ataques de tiempo y fuerza bruta.*
