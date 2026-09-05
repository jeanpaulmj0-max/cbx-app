import streamlit as st
import database
import mock_data
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(page_title="Cultura de Boxeo", page_icon="🥊", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Oswald', sans-serif; }
    h1, h2, h3 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 1px; color: #ffffff;}
    .stButton>button {
        width: 100%; border-radius: 4px; font-family: 'Bebas Neue', sans-serif;
        font-size: 1.2rem; background-color: #d11124; color: white; border: none;
    }
    .stButton>button:hover { background-color: #a00c1b; color: white; }
    .passport-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #444; border-left: 5px solid #d11124;
        color: white; margin-bottom: 20px;
    }
    .news-card { padding: 15px; background: #1a1a1a; border-radius: 8px; margin-bottom:15px; }
    .post-card { padding: 15px; background: #222; border-radius: 8px; margin-bottom:10px; border-left: 3px solid #666; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZACIÓN
# ==========================================
database.init_db()

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_data" not in st.session_state: st.session_state.user_data = None
if "view_noticia" not in st.session_state: st.session_state.view_noticia = None
if "comunidad_posts" not in st.session_state: st.session_state.comunidad_posts = mock_data.COMUNIDAD_POSTS_INICIALES

# ==========================================
# AUTENTICACIÓN
# ==========================================
def render_auth():
    st.markdown("<h1 style='text-align: center; color: #d11124; font-size: 4rem;'>CULTURA DE BOXEO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #888;'>FIGHT PASSPORT - ACCESO DIGITAL</h4><hr>", unsafe_allow_html=True)
    
    modo = st.radio("Acceso", ["Iniciar Sesión", "Registrar Pasaporte"], horizontal=True)
    
    if modo == "Iniciar Sesión":
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR AL RING"):
            if email and password:
                success, data = database.authenticate_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = data
                    st.rerun()
                else:
                    st.error(data)
            else:
                st.warning("Ingresa tus credenciales.")
                
    else:
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        email = st.text_input("Correo electrónico ")
        password = st.text_input("Contraseña ", type="password")
        password_conf = st.text_input("Confirmar Contraseña ", type="password")
        gym_origen = st.selectbox("¿Eres miembro de un Gimnasio Afiliado?", ["Independiente (Free)", "Socio - CBX Calpa", "Socio - Crossfit (Pro)"])
        
        if st.button("CREAR PASAPORTE"):
            if password != password_conf:
                st.error("Las contraseñas no coinciden.")
            else:
                success, msg = database.register_user(nombre, apellido, email, password, gym_origen)
                if success:
                    st.success(msg + ". Ya puedes iniciar sesión.")
                else:
                    st.error(msg)

# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
def render_dashboard():
    user = st.session_state.user_data
    
    col_logo, col_logout = st.columns([4, 1])
    with col_logo:
        st.markdown("<h2 style='color:#d11124; margin:0;'>CULTURA DE BOXEO</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("SALIR", key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.rerun()

    tab_perfil, tab_comunidad, tab_entrenamientos, tab_noticias, tab_fantasy, tab_tienda = st.tabs([
        "👤 RÉCORD", "💬 EL RING", "🥊 ACADEMIA", "📰 NOTICIAS", "🎯 FANTASY", "🛒 GEAR (USA)"
    ])
    
    # ------------------ TAB: PERFIL (RÉCORD DE PELEADOR) ------------------
    with tab_perfil:
        xp = user.get('xp', 0)
        nivel = (xp // 100) + 1
        xp_next = nivel * 100
        progreso_xp = (xp % 100)
        
        st.markdown(f"""
        <div class="passport-card">
            <h2 style='margin-top:0; color:#d11124; font-family: "Bebas Neue", sans-serif;'>RÉCORD DE PELEADOR</h2>
            <hr style='border-color:#444;'>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin: 0;">{user['nombre'].upper()} {user['apellido'].upper()}</h1>
                    <p style="color: #aaa; margin: 0;">Esquina: {user['gym_origen']}</p>
                </div>
                <div style="text-align: right;">
                    <h2 style="margin: 0; color: #FFD700;">NIVEL {nivel}</h2>
                    <small>{xp} / {xp_next} XP</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progreso_xp / 100.0, text="Progreso al siguiente nivel")
        
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            st.info(f"**TÍTULO ACTUAL:** {'Debutante' if nivel == 1 else 'Amateur' if nivel < 5 else 'Profesional'}")
            st.warning(f"**BOLSA ACTUAL:** {user['cbx_coins']} CBX Coins 🪙")
        with col_stats2:
            st.success("**LICENCIA:** " + ("Activa (Pro)" if user['rol'] == 'pro' else "Socio" if user['rol'] == 'member' else "Aficionado (Free)"))
            
        st.markdown("### 🏆 Recompensas Desbloqueadas")
        if nivel >= 1:
            st.markdown("- ✅ **Nivel 1:** Acceso al Ring (Foro) y Fantasy Picks.")
        if nivel >= 2:
            st.markdown("- ✅ **Nivel 2:** 10% de Descuento en Guantes Importados (Tienda).")
        else:
            st.markdown("- 🔒 **Nivel 2:** Alcanza el Nivel 2 para obtener 10% OFF en Guantes.")
        
        if nivel >= 5:
            st.markdown("- ✅ **Nivel 5:** Inscripción gratuita al Torneo Semestral.")
        else:
            st.markdown("- 🔒 **Nivel 5:** Alcanza el Nivel 5 para Torneos Gratuitos.")

    # ------------------ TAB: COMUNIDAD ------------------
    with tab_comunidad:
        st.header("El Ring")
        nuevo_post = st.text_area("¿Qué tienes en mente, campeón?", placeholder="Comparte tu entrenamiento o debate de boxeo...")
        if st.button("Publicar en El Ring"):
            if nuevo_post.strip():
                st.session_state.comunidad_posts.insert(0, {
                    "id": f"C{len(st.session_state.comunidad_posts)+1}",
                    "autor": f"{user['nombre']}_{user['apellido'][0]}",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "contenido": nuevo_post
                })
                st.success("Publicado.")
                st.rerun()
            else:
                st.warning("Escribe algo antes de publicar.")
                
        st.markdown("---")
        for post in st.session_state.comunidad_posts:
            st.markdown(f"""
            <div class='post-card'>
                <small style='color:#d11124;'><b>@{post['autor']}</b> • {post['fecha']}</small>
                <p style='margin-top:5px;'>{post['contenido']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ------------------ TAB: ENTRENAMIENTOS ------------------
    with tab_entrenamientos:
        st.header("Academia de Combate")
        st.markdown("<p style='color:#888;'>Estructuras de aprendizaje paso a paso. Únete a los próximos drops.</p>", unsafe_allow_html=True)
        
        for ruta, niveles in mock_data.ENTRENAMIENTOS.items():
            with st.expander(f"{ruta}", expanded=True):
                for t in niveles:
                    st.markdown(f"**{t['nivel_orden']}: {t['titulo']}** ({t['duracion']})")
                    
                    # Validar acceso
                    tiene_acceso = False
                    if t['acceso'] == 'free': tiene_acceso = True
                    elif t['acceso'] == 'member' and user['rol'] in ['member', 'pro']: tiene_acceso = True
                    elif t['acceso'] == 'pro' and user['rol'] == 'pro': tiene_acceso = True
                    
                    if tiene_acceso:
                        st.write(t['descripcion'])
                        st.caption(f"Objetivo: {t['objetivo']} | Equipo: {t['equipamiento']}")
                        
                        if t.get('estado') == 'proximamente' or not t.get('video_url'):
                            st.info(f"⏳ **PRÓXIMO DROP:** Disponible el {t.get('fecha_drop', 'Próximamente')}. ¡Mantente atento a la comunidad!")
                        else:
                            st.info(t['instrucciones'])
                            st.video(t['video_url'])
                    else:
                        st.error(f"🔒 Contenido exclusivo. Requiere nivel de acceso: {t['acceso'].upper()}")
                    st.markdown("---")

    # ------------------ TAB: NOTICIAS ------------------
    with tab_noticias:
        if st.session_state.view_noticia is None:
            st.header("Última Hora")
            for n in mock_data.NOTICIAS:
                st.markdown(f"""
                <div class='news-card'>
                    <h3 style='margin-top:0;'>{n['titulo']}</h3>
                    <p><i>{n['subtitulo']}</i></p>
                    <small>{n['categoria']} | {n['fuente']} | {n['fecha']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Leer Artículo", key=f"btn_leer_{n['id']}"):
                    st.session_state.view_noticia = n
                    st.rerun()
        else:
            n = st.session_state.view_noticia
            if st.button("← Volver al Feed de Noticias"):
                st.session_state.view_noticia = None
                st.rerun()
            st.image(n['imagen_url'], use_container_width=True)
            st.title(n['titulo'])
            st.markdown(f"**{n['subtitulo']}**")
            st.caption(f"{n['fecha']} | Fuente: {n['fuente']}")
            st.markdown(n['contenido_html'], unsafe_allow_html=True)
            st.info("Botón de compartir: Próximamente V1.1")

    # ------------------ TAB: FANTASY ------------------
    with tab_fantasy:
        st.header("Fantasy Picks")
        st.markdown(f"**Tu saldo actual:** {user['cbx_coins']} CBX Coins 🪙")
        st.warning("⚠️ Modo DEMO: Las apuestas reales y el sistema de ranking global llegarán en la V1.1. Tus picks actuales se guardan de manera local temporal.")
        for cart in mock_data.FANTASY_CARTELERAS:
            st.subheader(f"📅 {cart['titulo']}")
            for p in cart['combates']:
                st.markdown(f"{p['peleador_a']} vs {p['peleador_b']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"{p['peleador_a']} (x{p['cuota_a']})", key=f"f_{p['id']}_a"):
                        st.toast("Pick registrado (Simulación V1.0)", icon="✅")
                with col2:
                    if st.button(f"{p['peleador_b']} (x{p['cuota_b']})", key=f"f_{p['id']}_b"):
                        st.toast("Pick registrado (Simulación V1.0)", icon="✅")

    # ------------------ TAB: TIENDA ------------------
    with tab_tienda:
        st.header("Tienda Oficial")
        for prod in mock_data.TIENDA_PRODUCTOS:
            col_img, col_info = st.columns([1, 3])
            with col_img:
                st.markdown(f"<div style='font-size: 4rem; text-align:center;'>{prod['img']}</div>", unsafe_allow_html=True)
            with col_info:
                st.subheader(prod['nombre'])
                st.markdown(f"<h4 style='color:#d11124; margin:0;'>{prod['precio']}</h4>", unsafe_allow_html=True)
                st.write(prod['desc'])
                if st.button(f"Comprar", key=f"buy_{prod['id']}"):
                    st.info("La pasarela de pago (Checkout) se habilitará en la versión de producción.")
            st.markdown("---")

if __name__ == "__main__":
    if st.session_state.logged_in and st.session_state.user_data:
        render_dashboard()
    else:
        render_auth()
