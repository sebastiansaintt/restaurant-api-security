# Módulo 1: Seguridad en Autenticación y Hashing

**Integrante:** Sebastian (Member 1)  
**OWASP Cubierto:** API2:2023 (Broken Authentication), A02:2021 (Cryptographic Failures), A07:2021 (Auth Failures)

---

## Problema (Vulnerabilidad)
La aplicación original no tiene defensa robusta ante atauqes, entre ellos el tema de hashing, usa algoritmos de hashing rápidos y/o configuraciones por defecto permite a los atacantes usar fuerza bruta o GPUs para crackear contraseñas masivamente. Además, no había validación de fuerza de contraseña ni protección contra ataques de tiempo (Timing Attacks), lo que facilitaba el robo de cuentas.

*   **Impacto:** Fuga de base de datos (data breach) = robo de credenciales
*   **ETICA:** En colombia, la ley de proteccion de datos personales es requisito para la aseguranza de software o software de calidad ('Security by Design'). Dejar puertas abiertas por negligencia o ignorar los estándares de la industria (NIST/OWASP) compromete la confianza de los clientes y la moral del desarrollador


## PROPUESTA (Hardening y Mitigación)
Implementé un esquema de protección multicapa:

1.  **Políticas de Contraseñas (A07:2021):** uso de Regex para exigir criterios (caracteres, numeros, simbolos, etc.)
2.  **Hardening Criptográfico (A02:2021):** Migración a **Argon2id** (estandar actual) con parámetros "Memory-Hard" explícitos (`memory_cost=64MB`, `time_cost=3`). Esto frena en seco el cracking por GPU.
3.  **Defensa Anti-Timing Attacks:** Si un usuario no existe, el servidor calcula un hash "dummy" para que la respuesta tarde lo mismo, evitando que el atacante "adivine" usuarios midiendo milisegundos.
4.  **Tarpitting:** Cada intento fallido añade un retraso de 0.5s, desincentivando la fuerza bruta.

---

