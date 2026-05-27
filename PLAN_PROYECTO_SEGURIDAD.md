# Plan de Proyecto — Análisis, Explotación y Mitigación de Vulnerabilidades

**Curso:** Optativa · 2026-II  
**Repositorio base:** [Damn Vulnerable Restaurant API Game](https://github.com/theowni/Damn-Vulnerable-Restaurant-API-Game)  
**OWASP cubierto:** API Security Top 10 (2023) | OWASP Top 10 2021

---

## Checklist

| # | Actividad obligatoria | Responsable | Entregable |
|---|---|---|---|
| 1 | Selección del sistema vulnerable — descripción y propósito | Todos | README principal |
| 2 | Identificación y caracterización de cada vulnerabilidad | Cada integrante la suya | `member-X/README.md` |
| 3 | Análisis técnico y ético — origen + reflexión | Cada integrante la suya | `member-X/README.md` |
| 4 | Propuesta y aplicación de mitigación — refactorización + justificación | Cada integrante la suya | `member-X/fix/` |
| 5 | Validación — evidencia antes/después | Cada integrante la suya | `member-X/evidence/` |
| + | Publicación obligatoria en GitHub con contexto, vulnerabilidades, OWASP, soluciones y reflexión ética | Todos | `README.md` del repo |


---

## Asignación de vulnerabilidades (1 por integrante)

| Integrante | Vulnerabilidad | OWASP | Descripción rápida |
|---|---|---|---|
| 1 | Hashing débil de contraseñas | API2:2023 Broken Authentication | MD5 / SHA1 sin sal → reemplazar con bcrypt |
| 2 | JWT inseguro / algoritmo `none` | API2:2023 Broken Authentication | Token sin firma válida aceptado por el servidor |
| 3 | Sin rate limiting en login | API4:2023 Unrestricted Resource Consumption | Fuerza bruta posible → throttling + bloqueo |
| 4 | Escalada de privilegios vía token | API1:2023 Broken Object Level Authorization | Cliente cambia rol a `admin` manipulando payload |

---

## Estructura del repositorio del equipo

```
restaurant-api-security/
├── README.md                        ← publicación principal
├── vulnerable-app/                  ← clon del repo original
├── member-1-hashing/
│   ├── README.md                    ← ficha técnica: descripción, OWASP, impacto, ética
│   ├── evidence/
│   │   ├── before/                  ← capturas / scripts del ataque exitoso
│   │   └── after/                   ← capturas / scripts del ataque fallido post-mitigación
│   └── fix/
│       └── utils_fixed.py           ← código corregido con comentarios de justificación
├── member-2-jwt/
│   ├── README.md
│   ├── evidence/
│   │   ├── before/
│   │   └── after/
│   └── fix/
├── member-3-rate-limit/
│   ├── README.md
│   ├── evidence/
│   │   ├── before/
│   │   └── after/
│   └── fix/
├── member-4-authz/
│   ├── README.md
│   ├── evidence/
│   │   ├── before/
│   │   └── after/
│   └── fix/
└── docs/
    ├── owasp-mapping.md             ← tabla de mapeo vulnerabilidad → OWASP → mitigación
    └── ethical-reflection.md        ← reflexión ética del equipo (requerida en la publicación)
```

---

## Plan paso a paso

### Fase 0 — Setup compartido *(todos juntos, ~1 hora)*

**Paso 1 — Crear el repo del equipo en GitHub**

```bash
# En GitHub: crear repo vacío llamado "restaurant-api-security"
# Luego localmente:
mkdir restaurant-api-security
cd restaurant-api-security
git init
git remote add origin https://github.com/TU_USUARIO/restaurant-api-security.git
```

**Paso 2 — Crear la estructura de carpetas**

```bash
mkdir -p vulnerable-app
mkdir -p member-1-hashing/evidence/before member-1-hashing/evidence/after member-1-hashing/fix
mkdir -p member-2-jwt/evidence/before member-2-jwt/evidence/after member-2-jwt/fix
mkdir -p member-3-rate-limit/evidence/before member-3-rate-limit/evidence/after member-3-rate-limit/fix
mkdir -p member-4-authz/evidence/before member-4-authz/evidence/after member-4-authz/fix
mkdir -p docs
```

**Paso 3 — Clonar la app vulnerable dentro de la carpeta**

```bash
# Desde la raíz del repo del equipo:
git clone https://github.com/theowni/Damn-Vulnerable-Restaurant-API-Game vulnerable-app
```

**Paso 4 — Levantar la API con Docker y verificar**

```bash
cd vulnerable-app
docker-compose up -d

# Verificar que funciona:
# Abrir en navegador: http://localhost:8000/docs  (Swagger UI)
```

**Paso 5 — Primer commit y compartir con el equipo**

```bash
cd ..   # volver a la raíz del repo del equipo
echo "# Restaurant API Security Project" > README.md
git add .
git commit -m "chore: setup inicial del proyecto y estructura de módulos"
git push -u origin main

# Cada integrante hace fork del repo del equipo a su cuenta personal
```

---

### Fase 1 — Identificación *(cada quien en su módulo, ~2–3 horas)*

**Paso 6 — Encontrar el código vulnerable**

```bash
# Buscar hashing débil (integrante 1)
grep -r "md5\|sha1\|hashlib\|password" vulnerable-app/ --include="*.py" -n

# Buscar JWT (integrante 2)
grep -r "jwt\|decode\|encode\|secret\|algorithm" vulnerable-app/ --include="*.py" -n

# Buscar rate limiting ausente (integrante 3)
grep -r "login\|attempt\|limit\|throttle" vulnerable-app/ --include="*.py" -n

# Buscar autorización (integrante 4)
grep -r "role\|admin\|permission\|authorize" vulnerable-app/ --include="*.py" -n
```


**Paso 7 — Explotar la vulnerabilidad y guardar evidencia**

Cada integrante demuestra con Postman, curl o Python que la vulnerabilidad es real, y guarda las capturas en `member-X/evidence/before/`.

```bash
# Ejemplo: explotación JWT alg:none (integrante 2)
python3 - <<'EOF'
import base64, json

header = {"alg": "none", "typ": "JWT"}
payload = {"user_id": 1, "role": "admin"}  # escalada de rol

def b64(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")

fake_token = f"{b64(header)}.{b64(payload)}."
print("Token sin firma:", fake_token)
# Si el servidor acepta este token → vulnerabilidad confirmada
EOF
```

**Paso 8 — Escribir la ficha técnica en `member-X/README.md`**

Cada `README.md` de módulo debe tener estas secciones (las mismas que pide el profe en la rúbrica):

```markdown
# Vulnerabilidad: [Nombre]

## Descripción
Qué hace mal el código y cómo se manifiesta.

## Riesgo de seguridad
Qué puede ocurrir si se explota.

## Categoría OWASP
API Security Top 10 — APIx:2023 [Nombre categoría]

## Impacto potencial
Sobre el sistema, los datos y los usuarios.

## Origen de la vulnerabilidad
Diseño / implementación / configuración — explicar cuál y por qué.

## Reflexión ética
Responsabilidad del ingeniero de software frente a esta práctica insegura.

## Evidencia del ataque (antes)
[Capturas o descripción del exploit exitoso]

## Mitigación aplicada
[Ver carpeta fix/]

## Justificación técnica
Por qué esta solución mitiga el riesgo.

## Evidencia post-mitigación (después)
[Capturas o descripción del ataque fallido]
```

---

### Fase 2 — Mitigación *(cada quien en su módulo, ~3–4 horas)*

**Paso 9 — Copiar el archivo afectado a la carpeta del módulo**

```bash
# Ejemplo integrante 1:
cp vulnerable-app/app/auth/utils.py member-1-hashing/fix/utils_fixed.py

# Nunca editar nada dentro de vulnerable-app/
```

**Paso 10 — Aplicar la mitigación con comentarios de justificación**

```python
# === INTEGRANTE 1: Hashing débil → bcrypt ===

# ANTES (vulnerable) — MD5 sin sal, reversible con rainbow tables
import hashlib
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# DESPUÉS (mitigado)
import bcrypt

def hash_password(password: str) -> bytes:
    # bcrypt genera sal única automáticamente por cada hash
    # rounds=12 → ~300ms por intento, hace fuerza bruta computacionalmente inviable
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

def verify_password(plain: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed)
```

```python
# === INTEGRANTE 2: JWT alg:none → validación estricta ===

# ANTES (vulnerable)
import jwt
payload = jwt.decode(token, options={"verify_signature": False})  # sin verificar firma

# DESPUÉS (mitigado)
import jwt
SECRET_KEY = os.environ.get("JWT_SECRET")  # secreto desde variable de entorno, nunca hardcodeado

payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"],   # lista explícita — rechaza alg:none automáticamente
)
```

```python
# === INTEGRANTE 3: Rate limiting en endpoint de login ===

# ANTES (vulnerable) — sin límite de intentos
@app.post("/login")
def login(credentials: LoginSchema):
    ...

# DESPUÉS (mitigado) — con slowdown y bloqueo
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")   # máximo 5 intentos por minuto por IP
def login(request: Request, credentials: LoginSchema):
    ...
```

```python
# === INTEGRANTE 4: Escalada de privilegios — validar rol en servidor ===

# ANTES (vulnerable) — confiar en el rol que viene en el token sin verificar en DB
def get_current_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload  # el rol viene del token, no de la base de datos

# DESPUÉS (mitigado) — consultar siempre el rol real desde la base de datos
def get_current_user(token: str, db: Session):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401)
    return user  # rol siempre desde DB, no desde el token
```

**Paso 11 — Validar que la mitigación funciona**

Repetir exactamente el mismo ataque del Paso 7 contra el código corregido. Verificar que falla. Guardar capturas en `member-X/evidence/after/`.

---

### Fase 3 — Integración *(todos juntos, ~2 horas)*

**Paso 12 — Escribir el README principal del repositorio**

Este documento es la publicación obligatoria. Debe incluir:

- Contexto del problema (la app del restaurante y sus riesgos)
- Las 4 vulnerabilidades analizadas (enlazar a cada módulo)
- Tabla de mapeo vulnerabilidad → riesgo → OWASP → mitigación
- Reflexión técnica y ética del equipo

**Paso 13 — Preparar la sustentación (20 min, 4 personas)**

| Segmento | Tiempo | Responsable |
|---|---|---|
| Contexto del sistema y enfoque del equipo | 3 min | 1 persona (acordar quién) |
| Módulo 1: hashing — problema, exploit, fix | 3 min | Integrante 1 |
| Módulo 2: JWT — problema, exploit, fix | 3 min | Integrante 2 |
| Módulo 3: rate limiting — problema, exploit, fix | 3 min | Integrante 3 |
| Módulo 4: autorización — problema, exploit, fix | 3 min | Integrante 4 |
| Demo en vivo (antes vs después en Postman) | 5 min | Quien esté más cómodo |

> Cada integrante defiende solo su módulo. Si alguien no trabajó, su módulo vacío no afecta la nota de los demás.

---

## Hito de semana 9 — revisión formativa

Para la revisión parcial del profe, cada integrante debe tener listo:

- [x] Vulnerabilidad identificada con código fuente localizado
- [x] Evidencia del exploit en `member-X/evidence/before/`
- [x] Ficha técnica en `member-X/README.md` con descripción, OWASP y propuesta inicial de mitigación
- [ ] Mitigación aplicada (puede estar en progreso)

---

## Tabla de mapeo OWASP — resumen ejecutivo

| Vulnerabilidad | OWASP | Riesgo | Mitigación |
|---|---|---|---|
| Hashing débil (MD5) | API2:2023 | Credenciales reversibles con rainbow tables | bcrypt con sal, rounds ≥ 12 |
| JWT sin firma (alg:none) | API2:2023 | Acceso arbitrario a cualquier cuenta | HS256 obligatorio, lista de algoritmos explícita |
| Sin rate limiting | API4:2023 | Fuerza bruta automatizada sobre login | Throttling por IP, bloqueo temporal |
| Escalada de privilegios | API1:2023 | Cliente actúa como administrador | Rol siempre desde base de datos, nunca desde token |

---

*Documento generado como guía de trabajo del equipo. Última versión en el README del repositorio.*
