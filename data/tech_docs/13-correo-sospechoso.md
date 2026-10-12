# Correo sospechoso y suplantación

IT Support trata un correo o un mensaje que pide credenciales como un incidente, aunque venga de un nombre interno. People y Finance no "confirman por las dudas" una clave. Esta página es el runbook corto para la persona que recibió el mensaje.

## Señales

Se reporta de inmediato si el mensaje:

- pide la contraseña, el código de 6 dígitos o una foto del autenticador
- cambia de urgencia la cuenta bancaria del sueldo y apura a no usar el portal
- trae un archivo para "ver el recibo" o "actualizar la VPN"
- viene de un dominio parecido a nubiq.example, con una letra de más o de menos

El código de la app autenticadora no se dicta por teléfono. IT tampoco lo pide. Quien lo pide no es IT, aunque el número parezca local.

## Qué hacer

No se responde, no se abre el archivo y no se hace clic en el botón del correo. Se reenvía como adjunto, no como forward que vuelva a cargar las imágenes, a seguridad@nubiq.example, y se abre SOPORTE-INC. Si la persona ya escribió la contraseña, lo dice en el ticket en la primera línea. IT revoca las sesiones en ese momento y pide el cambio en acceso.nubiq.example.

Si ya se cambió la cuenta bancaria siguiendo el correo, se avisa en el mismo ticket y también a Finance, porque el pago puede estar por salir. IT no revierte una cuenta bancaria. Finance sí puede frenar una corrida que todavía no salió, si se entera antes del corte.

## Qué hace IT después

IT marca el mensaje, bloquea el dominio si es externo y revisa si otras personas lo recibieron. El aviso general sale por el canal de estado solo cuando hay más de un caso o un dominio nuevo. Un caso aislado se cierra con la persona y no se publica el nombre de quien cayó.

People mira el código de conducta solo si alguien interno mandó el pedido de claves a propósito. Un error de buena fe, avisado enseguida, no es una sanción. Esconder que se escribió la contraseña sí se trata como incumplimiento, porque alarga el incidente.

## Pruebas internas

IT puede mandar una simulación de correo, anunciada en el calendario del portal una vez por trimestre, sin decir el día. La simulación no pide un código real y no cambia cuentas. Quien hace clic llega a una página de IT que explica la pista, no a un formulario. Esas pruebas no descuentan vacaciones ni afectan la nota de desempeño.
