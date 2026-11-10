# Activar la nube (Supabase) — una sola vez, ~10 minutos

Con esto: lo que cargues o cambies en la app (rutas, tiendas, Excel) llega solo a los celulares de los empleados, y tú ves en **📊 Seguimiento** qué tiendas van, quién las hizo, notas, motivos y fotos.

1. **Cuenta y proyecto:** entra a supabase.com → New project (plan gratis). Elige una contraseña de base de datos cualquiera y la región más cercana.
2. **Tablas y permisos:** menú *SQL Editor* → New query. Abre `supabase_setup.sql`, cambia `TU_CORREO` por tu correo de administrador, pega todo y pulsa **Run**.
3. **Tu usuario administrador:** *Authentication → Users → Add user → Create new user*. Pon tu correo y una contraseña, y marca *Auto Confirm User*.
   Luego *Authentication → Sign In / Providers* y desactiva **Allow new users to sign up** (así nadie más puede crear cuentas).
4. **Claves:** *Project Settings → API*. Copia **Project URL** y la clave **anon / public** (NO la service_role).
5. **Conectar la app:** crea `cloud.json` (copia de `cloud.example.json`) con esos dos datos y ejecuta `python3 build.py`. Sube a GitHub: `index.html` y `sw.js`. (O pásame la URL y la clave anon y yo la genero.)

## Uso
- **Administrador:** 🔒 Administrador → correo y contraseña. Todo cambio que hagas se publica solo a los 3 segundos (o con ☁️ Publicar). La primera vez pulsa ☁️ Publicar.
- **Empleados:** la primera vez escriben su nombre. Cada foto y cada tienda hecha se envía sola; si no hay señal, queda en cola (⏳) y sale cuando vuelve internet. "Enviar informe" fuerza el envío.
- **Seguimiento:** 📊 Seguimiento se actualiza cada 15 s. Toca una tienda para ver piezas y fotos. 📥 Informe Excel baja todo con las fotos incrustadas.
- **Campaña nueva:** primero baja el Excel; luego 🗑 Borrar progreso y acepta borrar también en la nube. Los celulares de los empleados se limpian solos.

## Seguridad y límites
- Las fotos están en una carpeta privada: los empleados solo pueden subir; solo tú las ves.
- Los empleados no tienen cuenta: cualquiera que tenga el enlace de la app podría enviar avance. Para el uso interno de un equipo es suficiente; si quisieras cuentas por empleado se puede agregar.
- Plan gratis de Supabase: 1 GB de archivos (una campaña usa ~50 MB) y pausa el proyecto tras 1 semana sin uso; se reactiva desde su panel.
