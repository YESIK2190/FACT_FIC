import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Tablero de Operaciones", layout="wide")
st.title("📊 Tablero Interactivo de Operaciones")

archivo = st.file_uploader("Cargue archivo CSV o Excel", type=["csv","xlsx"])

if archivo is not None:
    try:
        if archivo.name.lower().endswith('.csv'):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo, engine='openpyxl')
    except ImportError:
        st.error("Falta instalar openpyxl. Verifique requirements.txt")
        st.stop()
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

    fecha_col='Fecha Grabacion Pago'
    proveedor_col='Proveedor'
    negocio_col='Negocio'
    gestor_col='Gestor'

    if fecha_col in df.columns:
        df[fecha_col]=pd.to_datetime(df[fecha_col], errors='coerce')

    filtrado=df.copy()

    st.sidebar.header('Filtros')
    for col in [proveedor_col, negocio_col, gestor_col]:
        if col in filtrado.columns:
            vals=st.sidebar.multiselect(col, sorted(filtrado[col].dropna().astype(str).unique()))
            if vals:
                filtrado=filtrado[filtrado[col].astype(str).isin(vals)]

    c1,c2,c3=st.columns(3)
    c1.metric('Total Operaciones', len(filtrado))
    c2.metric('Proveedores', filtrado[proveedor_col].nunique() if proveedor_col in filtrado.columns else 0)
    c3.metric('Gestores', filtrado[gestor_col].nunique() if gestor_col in filtrado.columns else 0)

    if fecha_col in filtrado.columns:
        d=filtrado.groupby(fecha_col).size().reset_index(name='Operaciones')
        st.altair_chart(alt.Chart(d).mark_line(point=True).encode(x=fecha_col,y='Operaciones'), use_container_width=True)

    a,b=st.columns(2)
    if proveedor_col in filtrado.columns:
        d=filtrado.groupby(proveedor_col).size().reset_index(name='Operaciones')
        a.altair_chart(alt.Chart(d).mark_bar().encode(x=proveedor_col,y='Operaciones'), use_container_width=True)

    if gestor_col in filtrado.columns:
        d=filtrado.groupby(gestor_col).size().reset_index(name='Operaciones')
        b.altair_chart(alt.Chart(d).mark_bar().encode(x=gestor_col,y='Operaciones'), use_container_width=True)

    if negocio_col in filtrado.columns:
        st.subheader('Operaciones por Negocio')
        st.dataframe(filtrado.groupby(negocio_col).size().reset_index(name='Operaciones'))

    st.subheader('Datos Filtrados')
    st.dataframe(filtrado, use_container_width=True)
else:
    st.info('Cargue un archivo para comenzar.')
