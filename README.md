# Recorrido Lonas P12

## Publicar en GitHub Pages
1. Sube a la raíz del repositorio: `index.html`, `manifest.json`, `sw.js`, `icon-192.png`, `icon-512.png`, `xlsx.full.min.js` y `exceljs.min.js`.
2. Settings → Pages → Deploy from a branch → `main` / `(root)`.
3. Abre `https://TU-USUARIO.github.io/NOMBRE-REPO/` en el celular.

## Datos desde Excel
Completa `Plantilla_Recorrido.xlsx` (hoja "Recorrido") y en la app pulsa **📥 Cargar Excel**.
La app arma rutas, tiendas, mapa, qué hacer, material y promoción. **📤 Bajar Excel** exporta lo actual.

Regenerar: `python3 build.py` (app) y `python3 make_template.py` (plantilla).

## Fotos e informe al cliente
En cada espacio: 📷 Antes / 📷 Después (abre la cámara, pone fecha, hora y tienda sobre la foto; en modo simple no se usa el GPS). Al tomar la foto "Después" el espacio se marca como hecho. **📸 Informe con fotos** genera un Excel con las fotos incrustadas y lo comparte (WhatsApp/correo) o lo descarga.

## Guardar el informe directo en GitHub
⚙️ GitHub → repositorio (usuario/repo, de preferencia PRIVADO), carpeta (evidencias) y token fine-grained con permiso Contents: Read and write solo para ese repositorio. Después, 📸 Informe con fotos sube el Excel a esa carpeta.

## Modo simple (empleados) y modo completo (administrador)
La app abre en **modo simple**: elegir ruta → una tienda a la vez → qué colocar → 📷 Antes → 📷 Después → siguiente. El modo completo solo se abre con el **PIN de administrador** (🔒 Administrador). Los empleados solo ven: ruta → tienda → fotos → enviar informe.
En modo completo: **✏️ Editar rutas** (ordenar tiendas, mover/quitar/agregar tiendas, crear/renombrar/borrar/ordenar rutas, tienda nueva, pieza nueva) y **🖨 PDF** por ruta o de todas, listo para imprimir (carta horizontal, casilla de hecho y notas).
Los cambios del editor se guardan en el celular. Para reiniciar: ♻ Originales.

## Borrar progreso y PDF
**🗑 Borrar progreso** (modo completo, o enlace al final de la pantalla de rutas) borra de una vez los hechos, fotos, notas y "no realizados" del celular; pide escribir BORRAR. Las rutas y tiendas no cambian.
**🖨 PDF** descarga directo en el dispositivo el recorrido de las rutas con el formato de impresión (carta horizontal).

## PIN de administrador
El PIN se define al generar la app: `python3 build.py 123456` (si no se indica, usa 483917). Después sube el nuevo `index.html` y `sw.js` a GitHub. Al volver a Modo simple, la sesión de administrador se cierra y hay que poner el PIN otra vez. Tras 5 intentos fallidos se bloquea 1 minuto.

## Nube (sincronización y seguimiento)
Ver `GUIA_NUBE.md`. Sin `cloud.json` la app funciona como antes (cada celular por separado). Con la nube, el administrador entra con correo y contraseña de Supabase (el PIN deja de usarse).
