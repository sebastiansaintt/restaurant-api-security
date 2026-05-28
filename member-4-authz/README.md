# Vulnerabilidad: Escalada de privilegios vía token

## Descripción

La vulnerabilidad encontrada en la aplicación permite que un usuario autenticado cambie su rol a otro con mayores privilegios mediante el endpoint `/users/update_role`.

El sistema únicamente validaba que el usuario no intentara asignarse el rol `CHEF`, pero no verificaba si el usuario autenticado tenía permisos suficientes para modificar roles.

Esto permitía que un usuario común escalara privilegios y obtuviera acceso a funcionalidades restringidas.

---

## Riesgo de seguridad

Un atacante podría modificar su rol y obtener permisos administrativos o de empleado dentro del sistema, comprometiendo la seguridad de la aplicación y el acceso a información sensible.

---

## Categoría OWASP

OWASP API Security Top 10 2023

### API1:2023 Broken Object Level Authorization

Esta categoría hace referencia a fallos de autorización donde el sistema no valida correctamente los permisos de los usuarios sobre ciertos recursos o acciones.

---

## Impacto potencial

- Acceso no autorizado a funcionalidades restringidas.
- Escalada de privilegios.
- Manipulación de información sensible.
- Riesgo de comprometer completamente el sistema.

---

## Origen de la vulnerabilidad

La vulnerabilidad se originó debido a una validación incompleta dentro del endpoint `/users/update_role`.

El código vulnerable únicamente impedía asignar el rol `CHEF`, pero no verificaba el rol real del usuario autenticado.

Código vulnerable:

```python
if user.role == models.UserRole.CHEF.value:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only Chef is authorized to add Chef role!",
    )
```

Esto permitía que un usuario autenticado modificara su rol a `EMPLOYEE`.

---

## Evidencia del ataque (Before)

Se creó un usuario normal llamado `yairon` y posteriormente se autenticó utilizando el endpoint `/token`.

Luego se utilizó el endpoint:

PUT /users/update_role

con el siguiente cuerpo JSON:

```json
{
  "username": "yairon",
  "role": "EMPLOYEE"
}
```

El servidor respondió exitosamente con código `200`, permitiendo la escalada de privilegios:

```json
{
  "username": "yairon",
  "role": "Employee"
}
```

Las capturas de evidencia fueron almacenadas dentro de:

```txt
member-4-authz/evidence/before/
```

---

## Mitigación aplicada

Se implementó una validación adicional para verificar el rol del usuario autenticado antes de permitir la modificación de roles.

Código corregido:

```python
if current_user.role != models.UserRole.CHEF:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only Chef is authorized to update user roles!",
    )
```

Con esta validación únicamente los usuarios con rol `CHEF` pueden modificar roles dentro del sistema.

---

## Justificación técnica

La solución implementada evita que usuarios comunes puedan modificar sus privilegios dentro del sistema.

Ahora el servidor valida el rol real del usuario autenticado antes de ejecutar la operación, impidiendo la escalada de privilegios.

---

## Evidencia después de la mitigación (After)

Después de aplicar la mitigación, se repitió exactamente el mismo ataque utilizando el endpoint `/users/update_role`.

Sin embargo, el servidor respondió:

```txt
403 Forbidden
```

y mostró el siguiente mensaje:

```json
{
  "detail": "Only Chef is authorized to update user roles!"
}
```

Esto demuestra que la vulnerabilidad fue corregida exitosamente.

Las capturas de evidencia posteriores a la mitigación fueron almacenadas dentro de:

```txt
member-4-authz/evidence/after/
```

---

## Reflexión ética

Los desarrolladores de software tienen la responsabilidad de implementar mecanismos adecuados de autorización y control de acceso.

Permitir que un usuario modifique sus privilegios representa un riesgo crítico para la seguridad de los sistemas y la privacidad de los usuarios.

Es fundamental validar siempre los permisos desde el servidor y no confiar únicamente en la información enviada por el cliente.