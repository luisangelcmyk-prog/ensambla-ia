"""ENSAMBLA IA: guía visual y registro de pruebas. Ejecutar: streamlit run app.py"""
import csv
import io
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
STEPS = [
    ("Base", "Coloca la placa de base sobre una superficie firme e identifica la ranura central."),
    ("Asa central", "Ubica el asa larga con abertura de agarre. Comprueba su orientación y alinéala con la base."),
    ("Soportes laterales", "Identifica las dos piezas estrechas. Alinea sus ranuras con las uniones correspondientes."),
    ("Placa intermedia", "Toma una placa con cuatro orificios e identifica las ranuras del nivel inferior."),
    ("Placa superior", "Coloca la segunda placa con cuatro orificios en las uniones superiores y comprueba estabilidad."),
]
st.set_page_config(page_title="ENSAMBLA IA", page_icon="🧩", layout="centered")
st.markdown("""<style>.stApp{background:#07151f;color:#ecfaf2}h1,h2,h3{color:#c2f99a!important}.stButton button{border-radius:12px}div[data-testid="stMetric"]{border:1px solid #355460;border-radius:12px;padding:10px}</style>""",unsafe_allow_html=True)
if "step" not in st.session_state: st.session_state.step = 0
if "events" not in st.session_state: st.session_state.events = []
if "notes" not in st.session_state: st.session_state.notes = []

def event(action, text=""):
    st.session_state.events.append({"fecha":datetime.now().isoformat(timespec="seconds"), "paso":st.session_state.step+1, "accion":action,"observacion":text})

def csv_bytes(rows):
    mem=io.StringIO(); w=csv.DictWriter(mem,fieldnames=["fecha","paso","accion","observacion"]); w.writeheader();w.writerows(rows);return mem.getvalue().encode('utf-8-sig')

def annotate(img, step):
    photo=img.convert("RGB").copy();d=ImageDraw.Draw(photo,"RGBA")
    w,h=photo.size;band=max(64,round(h*.10));d.rectangle((0,0,w,band),fill=(5,26,37,225));
    label=f"ENSAMBLA IA | Paso {step+1}/5: {STEPS[step][0]}";d.text((max(12,w//35),band//3),label,fill=(164,255,131,255),font=ImageFont.load_default(size=max(13,min(35,w//24))))
    d.rectangle((int(w*.14),int(h*.28),int(w*.86),int(h*.72)),outline=(158,255,112,220),width=max(3,w//200))
    return photo

st.caption("PROTOTIPO ACADÉMICO · VISUALIZACIÓN Y EVIDENCIAS")
st.title("ENSAMBLA IA")
st.write("Guía de armado del portavasos de madera. Usa las fotos reales como referencia y documenta qué funciona.")
st.info("Esta versión Streamlit captura fotografías y les añade guías 2D; NO identifica piezas automáticamente. Para cámara en vivo y detección de QR, abre la web móvil publicada con GitHub Pages.")
with st.expander("📷 Ver las piezas reales",expanded=False):
    st.image(str(ROOT/"assets/piezas.jpg"),caption="Piezas desmontadas; equipo de trabajo",use_container_width=True)
    st.image(str(ROOT/"assets/armado.jpg"),caption="Estructura montada; referencia",use_container_width=True)

step=st.session_state.step
st.progress((step+1)/len(STEPS),text=f"Paso {step+1} de {len(STEPS)}")
st.subheader(STEPS[step][0]);st.write(STEPS[step][1]);st.caption("Orden propuesto a partir de fotografías; validar con la persona que fabricó las piezas.")
c1,c2=st.columns(2)
with c1:
    if st.button("← Anterior",disabled=step==0,use_container_width=True):st.session_state.step-=1;st.rerun()
with c2:
    if st.button("Siguiente →",disabled=step==len(STEPS)-1,use_container_width=True):event("paso confirmado manualmente");st.session_state.step+=1;st.rerun()
st.markdown("### Captura una evidencia")
source=st.radio("Origen de imagen",["Cámara","Subir fotografía"],horizontal=True)
photo=st.camera_input("Apunta a las piezas") if source=="Cámara" else st.file_uploader("Sube una foto",type=["jpg","jpeg","png"])
if photo:
    img=Image.open(photo)
    annotated=annotate(img,step)
    st.image(annotated,caption="Foto con encuadre y etiqueta del paso (no es detección automática)",use_container_width=True)
    out=io.BytesIO();annotated.save(out,format="PNG")
    st.download_button("⬇ Descargar evidencia anotada",out.getvalue(),file_name=f"evidencia_paso_{step+1}.png",mime="image/png")
st.markdown("### Registro del experimento")
with st.form("record"):
    outcome=st.selectbox("Resultado",["Funcionó","Funcionó parcialmente","Falló"])
    notes=st.text_area("¿Qué funcionó, qué falló y qué cambiarías?")
    if st.form_submit_button("Registrar observación"):
        event(outcome,notes);st.success("Observación agregada al registro de esta sesión.")
if st.session_state.events:
    st.dataframe(st.session_state.events,use_container_width=True,hide_index=True)
    st.download_button("⬇ Descargar registro CSV",csv_bytes(st.session_state.events),file_name="experimento_ensambla_ia.csv",mime="text/csv")
st.markdown("### Marcador de prueba")
st.image(str(ROOT/"assets/marcador_base.png"),width=210,caption="QR de la base para la web móvil")
st.caption("Los datos del registro permanecen solo en la sesión actual hasta que se descargan. Evita cerrarla antes de exportar.")
