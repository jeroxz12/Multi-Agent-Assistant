# Cuentas, contraseñas y autenticador

IT Support administra las cuentas de Nubiq. La contraseña no se envía por el canal de un equipo ni por correo. People Operations no la pide y no la guarda.

## Renovación

La contraseña de acceso.nubiq.example vence a los 90 días. El aviso llega 7 días antes al correo de la empresa. Si venció, el cliente VPN muestra NT-401 y el correo deja de aceptar la clave anterior.

El cambio se hace en acceso.nubiq.example con el código de 6 dígitos de la app autenticadora. La nueva contraseña tiene al menos 14 caracteres, una mayúscula, un número y un símbolo. No se reutilizan las últimas 5.

## App autenticadora

La app oficial es la que IT indica en el portal, sección Autenticador. El alta inicial ocurre el día 1, con el ticket SOPORTE-ONB. Si se pierde el teléfono, no hay código de respaldo por SMS. Se abre SOPORTE-MFA. IT verifica la identidad con el manager en una llamada y emite un alta nueva. El alta anterior queda invalidada en el momento.

Un código de 6 dígitos dura 30 segundos. Si el reloj del teléfono está mal, los códigos no coinciden. Antes de abrir el ticket, se activa la hora automática del teléfono y se prueba un código nuevo.

## Correo y bloqueo

Después de 8 intentos fallidos en 15 minutos, la cuenta queda bloqueada. El desbloqueo es el ticket SOPORTE-CUENTA. IT no desbloquea por un mensaje directo sin ese ticket, aunque el pedido lo haga un manager.

El correo de recuperación es el correo personal cargado en el portal IT, que la persona puede editar estando autenticada. Si no puede entrar y el correo personal está viejo, el manager confirma la identidad y IT lo actualiza. Ese cambio queda en el registro del ticket.

## Cuentas de servicio

Las cuentas compartidas de un sistema, como un buzón de alertas, no usan la app autenticadora de una persona. Las administra IT y la contraseña rota cada 60 días. Pedir "la clave del buzón de alertas" en un canal abierto se rechaza. El acceso se otorga al rol, no se copia la clave.

## Sesiones

Cerrar la sesión de un equipo perdido se hace desde el portal IT, Mis sesiones, si todavía hay otra sesión viva. Si no hay ninguna, el camino es SOPORTE-CUENTA y IT revoca todas las sesiones. La laptop perdida también se informa a People Operations el mismo día, porque People abre el registro interno. El bloqueo técnico lo hace IT, no People.
