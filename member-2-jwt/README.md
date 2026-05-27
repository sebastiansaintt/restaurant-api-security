 # Análisis y Mitigación de Vulnerabilidad JWT

 ## 1. Descripción General

En este módulo se analiza una vulnerabilidad crítica en la autenticación de la API relacionada con el uso inseguro de JSON Web Tokens (JWT).

El problema principal radica en que la aplicación no verificaba la firma del token, lo que permitía aceptar tokens manipulados o falsificados.

## 2. Vulnerabilidad Identificada
### Ubicación:

Archivo: jwt_auth.py

### Código vulnerable:
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    options={"verify_signature": False},
)

## 3. Riesgo de Seguridad

Esta implementación genera una vulnerabilidad crítica porque:

No se valida la autenticidad del token
Se pueden modificar los datos internos del JWT
El sistema acepta tokens falsos

### Posibles ataques:
Suplantación de identidad
Acceso como otro usuario (ej: admin)
Escalación de privilegios
Acceso a información sensible

## 4. Mitigación Aplicada (JWT)
### Solución implementada:

Se eliminó completamente la opción insegura verify_signature.

### Código corregido:
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
)
### Resultado:
Se obliga a validar la firma del token
Solo tokens legítimos son aceptados
Se elimina la posibilidad de falsificación
## 5. Vulnerabilidad en la Clave Secreta

### Ubicación:

Archivo: config.py

### Código vulnerable:
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", generate_random_secret())
def generate_random_secret():
    return "".join(random.choices("1234567890", k=6))

### Problemas detectados:
Clave de solo 6 caracteres
Solo números
Fácil de romper por fuerza bruta
Uso de random (no seguro)
La clave cambia en cada ejecución

## 6. Mitigación Aplicada (Clave)
### Código corregido:

JWT_SECRET_KEY = "clave_super_segura_2026"

### Beneficios:
Mayor complejidad de la clave
Mayor seguridad contra ataques
Estabilidad del sistema
Tokens siguen siendo válidos entre ejecuciones