# ENSAMBLA IA · Prototipo de armado asistido

Prototipo académico para un portavasos de madera de **seis piezas físicas** (asa, base, dos placas con cuatro orificios y dos soportes estrechos). Incluye dos aplicaciones complementarias:

1. **`web/index.html`**, web móvil con cámara en vivo (`getUserMedia`), búsqueda de **un marcador QR**, guía visual 2D superpuesta, cinco pasos, captura de evidencia y CSV. Publicable con **GitHub Pages**.
2. **`app.py`**, aplicación **Streamlit** con instrucciones, fotos reales, cámara para instantáneas, anotación 2D y registro CSV del experimento. Publicable en **Streamlit Community Cloud**.

## Limitaciones reales

- Detectar el **QR** no significa identificar automáticamente las piezas de madera.
- El rectángulo de guía 2D no está anclado geométricamente a las piezas. Es una ayuda visual, no seguimiento de realidad aumentada 3D.
- Los pasos de armado son una **hipótesis basada en fotos**. Confirmar el orden y las orientaciones con quien fabricó el portavasos.
- La cámara requiere permisos del usuario y normalmente **HTTPS** o localhost. La detección QR web usa la biblioteca `jsQR` cargada desde CDN; necesita conexión a internet. Si falla, sigue funcionando la guía de pasos.
- El QR debe ser legible y estar visible. La detección se hace en el propio navegador; no se suben imágenes al servidor.
- Los registros CSV se descargan manualmente; no hay base de datos ni identificación de usuarios.

## Publicar el proyecto en GitHub (para principiantes)

1. Descarga y descomprime `ensambla-ia.zip`.
2. En https://github.com crea un repositorio, por ejemplo `ensambla-ia`, preferiblemente **público** para usar GitHub Pages sin complicaciones.
3. En la página del repositorio, elige **Add file → Upload files**. Sube **el contenido de la carpeta descomprimida** (no el ZIP); deben quedar `app.py`, `requirements.txt`, `README.md`, `web/` y `assets/` en la raíz. Haz **Commit changes**.
4. Para la web móvil: **Settings → Pages → Build and deployment → Deploy from a branch**, selecciona `main` y carpeta `/(root)` → **Save**.
5. Después de publicarse, abre `https://TU_USUARIO.github.io/ensambla-ia/web/` en el celular (sustituye TU_USUARIO y el nombre si es diferente).
6. Toca **Activar cámara**, acepta permiso, imprime `assets/marcador_base.png` y coloca el QR junto a la base. Apunta con el celular y comprueba el indicador **QR identificado ✓**.

## Publicar Streamlit

1. Con el repositorio ya creado, visita https://share.streamlit.io y entra con GitHub.
2. **Create app** → selecciona repositorio y rama `main`.
3. En **Main file path** escribe exactamente `app.py`.
4. Despliega. Streamlit instalará las dependencias desde `requirements.txt`.
5. Abre la dirección terminada en `.streamlit.app`. Prueba **Cámara**, la anotación y **Descargar registro CSV**.

## Ejecutar Streamlit en tu computador (opcional)

Con Python instalado, abre una terminal dentro de la carpeta:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Se abrirá `http://localhost:8501`. En el celular es mejor usar la versión publicada con HTTPS.

## Experimento de incertidumbre para presentar

**Pregunta:** ¿Puede el teléfono detectar de forma estable un marcador QR junto a la base y mostrar instrucciones útiles durante el ensamblaje?

**Materiales:** portavasos desarmado, 1 celular, QR impreso, navegador y una persona que haga el ensayo.

**Prueba:**
1. Abre la versión web en el celular y activa la cámara.
2. Muestra el QR junto a la base en diferentes distancias e iluminaciones. Registra si el estado cambia a `QR identificado ✓`.
3. Completa el montaje siguiendo los cinco pasos y toma capturas con **Guardar evidencia**.
4. Anota si fue fácil utilizar el teléfono mientras se manipulaban piezas y si alguna instrucción fue ambigua.
5. Descarga el CSV y reúne capturas/fotografías. Resume **funcionó / falló / se cambió**.

**Criterios por verificar:** detectar QR; recuperar detección tras ocultarlo; comprender instrucciones; trabajar con manos ocupadas; compatibilidad con otro celular.

**No afirmar:** que identifica piezas sin marcador, que valida ensamblaje automáticamente o que hay anclaje 3D real.

## Archivos

```text
ensambla-ia/
├── app.py                     # Streamlit + Python
├── requirements.txt           # Bibliotecas Python
├── README.md                  # Tutorial
├── .gitignore
├── assets/
│   ├── piezas.jpg             # Foto real de 6 piezas
│   ├── armado.jpg             # Foto real de objeto montado
│   └── marcador_base.png      # QR imprimible
└── web/
    └── index.html             # HTML + CSS + JavaScript, cámara en vivo
```

## Siguiente fase después del experimento

Entrenar un clasificador de imágenes con fotografías individuales de cada tipo de pieza y condiciones distintas, evaluar confusiones y, después, investigar AR con seguimiento espacial (p. ej. un SDK compatible). Esa funcionalidad **todavía no forma parte** de este prototipo.
