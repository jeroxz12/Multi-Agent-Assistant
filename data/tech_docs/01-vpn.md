# VPN de Nubiq

IT Support administra el acceso remoto. El cliente oficial se llama Nubiq Tunnel. No se usa otro cliente ni una extensión del navegador. People Operations no resetea la VPN y Finance no aprueba excepciones de acceso.

## Qué revisar primero

Si no podés conectarte desde casa, el orden es este:

1. Confirmá que el dispositivo está en la lista de equipos aprobados del portal IT, sección Mis equipos.
2. Cerrá Nubiq Tunnel por completo y volvé a abrirlo. No alcanza con pausar la conexión.
3. El segundo factor es el código de 6 dígitos de la app autenticadora. No llega por SMS ni por correo.
4. Si el cliente muestra NT-401, la contraseña de acceso venció. Se renueva en acceso.nubiq.example, no dentro del cliente.
5. Si muestra NT-403, el dispositivo no está registrado. El alta la hace IT con el ticket SOPORTE-VPN y no es automática.

Después de esos cinco pasos, si sigue sin conectar, se abre SOPORTE-VPN. En el ticket van el código de error, el sistema operativo y si el fallo es en la red de casa o también en datos móviles.

## Redes de casa

Nubiq Tunnel funciona sobre Wi-Fi doméstico y sobre datos móviles. Un router que bloquee UDP puede impedir el túnel. La prueba que pide IT es simple: compartir internet desde el teléfono y probar de nuevo. Si ahí conecta, el bloqueo está en el router de casa y el ticket se marca como red local, no como caída del servicio.

La VPN no se comparte. Un código de la app autenticadora no se reenvía a otra persona, ni a IT. Si alguien lo pide, se corta la conversación y se abre un incidente de cuenta.

## Horario del servicio

El servicio de VPN se monitorea de 9 a 19, hora de Argentina, los días hábiles. Fuera de ese horario hay guardia solo para una caída total, cuando Nubiq Tunnel falla para más de un equipo a la vez. Un NT-401 de una sola persona espera al siguiente día hábil, salvo que esa persona esté en una guardia de Soporte ya publicada.

## Equipos personales

Un teléfono personal puede tener la app autenticadora. La laptop desde la que se abre el túnel tiene que ser la entregada por IT, o una excepción escrita en el portal IT. Una laptop personal sin esa excepción recibe NT-403 aunque la contraseña sea correcta.

## Qué no resuelve esta página

Los días de vacaciones, el estipendio de trabajo remoto y la fecha de pago del sueldo no están acá. IT solo restablece el acceso. Si el portal Personas no abre y el error es de contraseña, el camino sigue siendo esta página. Si el portal abre y la duda es cómo cargar vacaciones, la respuesta es de People Operations.
