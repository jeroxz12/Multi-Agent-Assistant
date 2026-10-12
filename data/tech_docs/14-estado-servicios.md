# Estado de los servicios internos

IT Support publica el estado de los servicios que la empresa usa para trabajar. No es el estado del producto que ven los clientes: ese tablero lo mira Soporte. Esta página dice dónde mirar antes de abrir un ticket duplicado.

## Dónde se mira

El canal de estado y la página Estado del portal IT muestran tres valores por servicio: operativo, degradado o caído. Se actualizan cuando hay un cambio, no en un horario fijo. Si el servicio figura operativo y una sola persona falla, el problema es de esa cuenta o de ese equipo y corresponde un ticket individual.

Los servicios listados son: correo, Nubiq Tunnel, portal IT, portal Personas, portal Finance, repositorio y videollamada. Un servicio que no está en la lista no tiene tablero. Su fallo entra directo como SOPORTE-SOFT.

## Caída de la VPN para todos

Si Nubiq Tunnel figura caído, no se prueban los pasos de NT-401 uno por uno en diez tickets. Se espera el aviso del canal de estado. IT actualiza cada 60 minutos, igual que en un P1. Cuando vuelve a operativo, cada persona cierra el cliente y lo abre de nuevo. No hace falta un ticket por ese reinicio.

Un NT-403 durante una caída general sigue siendo un dispositivo no registrado. La caída no lo explica. Ese caso sí lleva SOPORTE-VPN cuando el tablero ya dice operativo, o se anota en el incidente si el tablero sigue en caído y IT pide no abrir tickets.

## Portal Finance degradado

Si el portal Finance está degradado, los formularios pueden fallar al guardar. IT lo anuncia. Finance, en ese caso y solo en ese caso, acepta facturas por facturas@nubiq.example. Un reintegro de viaje espera a que el portal vuelva, salvo que el plazo de 10 días hábiles se cumpla durante la caída. Si eso pasa, Finance deja constancia de la caída publicada por IT y acepta el pedido el día en que el portal vuelve, sin aplicar el rechazo por plazo.

IT no extiende plazos de Finance por su cuenta. Solo publica la hora de inicio y de fin de la degradación.

## Después de una caída

Al día hábil siguiente IT deja en Estado una línea con la hora de inicio, la hora de recuperación y el servicio. No incluye nombres de personas ni montos. Quien necesite esa hora para un plazo de Finance o de People cita esa línea. No hace falta un certificado aparte de IT.
