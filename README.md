# appparqcentra

App para celular (Android y iPhone) para monitorear **ParqControl** desde cualquier lugar. Está en la carpeta [`movil/`](movil/).

No modifica el programa de la computadora central. Se conecta a la misma API local que usa su pantalla web (`/api/boot`, `/api/login`, `/api/col`, `/api/doc`) y **solo lee** datos: no cobra, no abre cajas, no cambia nada.

## Qué muestra

- **Hoy:** lo cobrado, el neto, los gastos, los vehículos dentro contra la capacidad, las cajas abiertas, los pendientes y las pérdidas. También el desglose por forma de pago y por usuario, los últimos cobros, los gastos, los cancelados y el total del mes.
- **Dentro:** cada vehículo que está adentro, con su hora de entrada, el tiempo que lleva y lo que pagaría si saliera ahora. Los que pasan de 24 h salen en rojo.
- **Cajas:** las cajas abiertas, con cuánto efectivo debería haber en vivo, y los cierres recientes con faltante o sobrante.
- **Pendientes:** las salidas con pago pendiente, separando las vencidas.
- **Avisos:** si el sistema está encendido o no, las alertas de datos alterados, si los datos están bloqueados y si la licencia está por vencer.

Los datos se actualizan cada 15 segundos mientras la app está abierta, y también al deslizar hacia abajo. Los cálculos se copiaron de la pantalla de ParqControl 1.3, así que los totales deberían coincidir con los de la PC central.

## Verlo desde fuera del parqueo (Tailscale)

ParqControl solo escucha en la red local. Para entrar desde internet sin abrir puertos en el router, la forma más sencilla y segura es Tailscale, que es gratis para uso personal:

1. En la **computadora central**, instala Tailscale (https://tailscale.com/download) e inicia sesión.
2. En el **celular**, instala la app de Tailscale con la misma cuenta y déjala conectada.
3. En la app de Tailscale aparece la IP de la PC central (empieza con `100.`). En ParqControl Monitor, pon como dirección `http://100.x.x.x:8090`.
4. Puede que el Firewall de Windows bloquee la conexión que entra por Tailscale. Si es así, permite ParqControl también en esa red, o agrega una regla de entrada para el puerto 8090.

Si quieres HTTPS, en la PC central puedes correr `tailscale serve --bg 8090` y usar la dirección `https://nombre-pc.tu-red.ts.net` que te da.

**No** expongas el puerto 8090 directo a internet (redirección de puertos en el router). La API de ParqControl no fue hecha para eso.

Dentro del parqueo, con el mismo wifi, también sirve la dirección que sale abajo en la pantalla de ParqControl (`http://192.168.x.x:8090`).

## Usuario y PIN

Si ParqControl exige sesión para leer los datos, la app entra con `POST /api/login` usando el usuario y el PIN que pongas, y vuelve a entrar sola si la sesión se cae. No pude comprobar con el programa real si hace falta o no, porque no tengo una licencia activa para correrlo. Por eso esos campos son opcionales.

## Probar y compilar

Todo se hace desde la carpeta `movil/`:

```bash
cd movil
npm install

# servidor falso con datos inventados (imita la API de ParqControl)
npm run servidor-prueba                 # sin login
PEDIR_LOGIN=1 npm run servidor-prueba   # exige Admin / 1234

# abrir la app en modo desarrollo
npx expo start
```

La app usa `expo-secure-store`, que no viene en Expo Go, así que para probarla en un teléfono hace falta una *development build* o compilarla. Lo más fácil es compilar en la nube con EAS, sin Android Studio ni Mac:

```bash
npx eas-cli@latest login
npx eas-cli@latest build -p android --profile preview      # te da un .apk para instalar directo
npx eas-cli@latest build -p ios --profile production       # necesita cuenta Apple Developer (99 USD/año)
```

Para iPhone, la forma de instalarla es por TestFlight o por la App Store. Las dos piden la cuenta de Apple Developer.

Antes de publicar, cambia el identificador `com.parqcontrol.monitor` en `movil/app.json` por uno tuyo, y reemplaza los íconos de `movil/assets/`, que todavía son los de la plantilla de Expo.

## Lo que todavía no hace

- **Notificaciones con la app cerrada** (por ejemplo, "se cerró una caja con faltante"). Para eso hace falta un servicio en la PC central o en la nube que vigile los datos y mande los avisos push. ParqControl no lo trae y sin su código fuente no se le puede agregar.
- **Historial de días anteriores.** Por ahora muestra el día de hoy y el total del mes.
