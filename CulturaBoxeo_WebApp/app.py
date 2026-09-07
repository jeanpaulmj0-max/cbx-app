import streamlit as st
import database
import mock_data
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(page_title="ROUNDS BY CBX", page_icon="🥊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@300;400;700&display=swap');
    
    /* Animación 10x y Fondo de Cine de Boxeo */
    .stApp {
        background: linear-gradient(rgba(15, 10, 10, 0.85), rgba(25, 5, 5, 0.95)), url('https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?q=80&w=2000') no-repeat center center fixed !important;
        background-size: cover !important;
    }
    
    /* Tipografía Global - Evitando dañar los iconos de Streamlit */
    html, body, p, label, input, li { font-family: 'Oswald', sans-serif; color: #ffffff; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 1px; color: #ffffff !important;}
    
    /* Forzar fondo oscuro y texto claro en Expanders */
    div[data-testid="stExpander"] details { background-color: rgba(30,30,30,0.9); border: 1px solid #444; border-radius: 8px; }
    div[data-testid="stExpander"] summary { color: #FFD700 !important; background-color: transparent !important;}
    div[data-testid="stExpander"] summary svg { fill: #FFD700 !important; }
    .stButton>button {
        width: 100%; border-radius: 4px; font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.2rem; background-color: #d11124; color: white; border: none;
    }
    .stButton>button:hover { background-color: #a00c1b; color: white; }
    
    /* Botones secundarios (como los de El Ring) para que no sean rojos bloque */
    button[kind="secondary"] {
        background-color: transparent !important;
        border: 1px solid #555 !important;
        color: #fff !important;
    }
    button[kind="secondary"]:hover { border-color: #FFD700 !important; color: #FFD700 !important; }
    .stButton>button:hover { background-color: #a00c1b; color: white; }
    .passport-card {
        background: linear-gradient(135deg, rgba(30,30,30,0.9) 0%, rgba(42,42,42,0.9) 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #444; border-left: 5px solid #d11124;
        color: white; margin-bottom: 20px;
    }
    .news-card { padding: 15px; background: rgba(26,26,26,0.9); border-radius: 8px; margin-bottom:15px; }
    .post-card { padding: 15px; background: rgba(34,34,34,0.9); border-radius: 8px; margin-bottom:10px; border-left: 3px solid #666; }
    
    /* E-Commerce Card Style */
    .product-card {
        background-color: rgba(17,17,17,0.9);
        border: 1px solid #333;
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.2s, border-color 0.2s;
        margin-bottom: 20px;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
    }
    .product-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .product-info {
    /* Ocultar Branding y Menús de Streamlit para ilusión de App Nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    
    <!-- PWA / NATIVE APP INJECTION -->
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Rounds CBX">
    <link rel="apple-touch-icon" href="https://images.unsplash.com/photo-1599552375246-24ee029302e3?q=80&w=256&h=256&fit=crop">
    <link rel="shortcut icon" href="https://images.unsplash.com/photo-1599552375246-24ee029302e3?q=80&w=64&h=64&fit=crop">
""", unsafe_allow_html=True)

# ==========================================
# SIMULADOR DE BASE DE DATOS LOCAL (PARA TRANSICIÓN A SUPABASE)
# ==========================================
POSTS_INICIALES = [
    {"id": "C3", "autor": "BoxFan_99", "fecha": "Hace 5 minutos", "contenido": "**[Debate de Peleas]**<br>¿Alguien más piensa que a Canelo ya no le quedan rivales de verdad en 168? Debería subir a 175 otra vez o pelear con Benavidez ya. ¿Qué opinan?"},
    {"id": "C2", "autor": "Tyson_Fan", "fecha": "Hace 2 horas", "contenido": "**[Cine de Boxeo y Arte IA]**<br>Acabo de ver la nueva peli de boxeo. La fotografía es increíble, pero los movimientos en el ring se ven muy falsos. Faltó asesoría de peleadores reales."},
    {"id": "C1", "autor": "Rounds_Oficial", "fecha": "Hace 5 horas", "contenido": "**[Entrenamientos]**<br>¡Bienvenidos a la comunidad! Compartan aquí sus videos de sparring, dudas técnicas o especulaciones. Los usuarios con mejores aportes recibirán monedas semanales."}
]

TIENDA_DB = [
    {"id": "P1", "nombre": "Guantes Hayabusa T3 16oz", "precio": "$160.00", "categoria": "Guantes", "img_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=500&q=80", "desc": "Soporte de muñeca patentado V-Strap. (Importación directa)."},
    {"id": "P2", "nombre": "Cleto Reyes Entrenamiento 14oz", "precio": "$220.00", "categoria": "Guantes", "img_url": "https://images.unsplash.com/photo-1512686125587-578d1cbbe190?auto=format&fit=crop&w=500&q=80", "desc": "Piel de cabra auténtica, hechos a mano. El guante de los campeones."},
    {"id": "P3", "nombre": "Winning Professional 16oz", "precio": "$380.00", "categoria": "Guantes", "img_url": "https://images.unsplash.com/photo-1596328222879-11ba106bb983?auto=format&fit=crop&w=500&q=80", "desc": "La marca #1 del mundo. Máxima protección de nudillos."},
    {"id": "S1", "nombre": "Creatina Nutrex Research 300g", "precio": "$30.00", "categoria": "Suplementos", "img_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=500&q=80", "desc": "Creatina monohidratada pura. Beneficio PRO: 15% de Descuento."},
    {"id": "S2", "nombre": "Ronnie Coleman Signature Whey", "precio": "$75.00", "categoria": "Suplementos", "img_url": "https://images.unsplash.com/photo-1579722820308-d74e571900a9?auto=format&fit=crop&w=500&q=80", "desc": "Proteína premium para recuperación muscular. Sabor Vainilla."},
    {"id": "I1", "nombre": "Saco Pesado Everlast 100lbs", "precio": "$120.00", "categoria": "Sacos e Implementos", "img_url": "https://images.unsplash.com/photo-1517838503506-3b561768809d?auto=format&fit=crop&w=500&q=80", "desc": "Trabajo de potencia extrema."},
    {"id": "A1", "nombre": "Vendas Profesionales Ringside", "precio": "$15.00", "categoria": "Artículos de Entrenamiento", "img_url": "https://images.unsplash.com/photo-1595252876632-478a59483dc8?auto=format&fit=crop&w=500&q=80", "desc": "Mezcla semi-elástica para protección perfecta."}
]

ACADEMIA_DB = {
    "🔥 DROP 1: FUNDAMENTOS DEL STRIKING": [
        {"id": "T01", "titulo": "Postura, Guardia y Desplazamiento", "nivel_orden": "Episodio 1", "descripcion": "La base de todo peleador.", "duracion": "10 min", "objetivo": "Técnica", "equipamiento": "Ninguno", "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre", "instrucciones": "Próximamente", "acceso": "free"},
        {"id": "T02", "titulo": "Mecánica del Jab y Recto", "nivel_orden": "Episodio 2", "descripcion": "El 1-2. Poder desde la cadera.", "duracion": "15 min", "objetivo": "Poder", "equipamiento": "Ninguno", "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre", "instrucciones": "Próximamente", "acceso": "free"}
    ],
    "🥊 RUTINAS CBX STUDIO": [
        {"id": "T03", "titulo": "HIIT Boxeo: Sombra", "nivel_orden": "Rutina 1", "descripcion": "Quema de calorías máxima.", "duracion": "20 min", "objetivo": "Cardio", "equipamiento": "Ninguno", "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre", "instrucciones": "Próximamente", "acceso": "member"}
    ]
}

# ==========================================
# INICIALIZACIÓN
# ==========================================
database.init_db()

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_data" not in st.session_state: st.session_state.user_data = None
if "view_noticia" not in st.session_state: st.session_state.view_noticia = None
if "comunidad_posts" not in st.session_state: st.session_state.comunidad_posts = POSTS_INICIALES
if "mis_apuestas" not in st.session_state: st.session_state.mis_apuestas = []

# ==========================================
# AUTENTICACIÓN
# ==========================================
def render_auth():
    st.markdown("<h1 style='text-align: center; color: #d11124; font-size: 4rem; margin-bottom:0;'>ROUNDS BY CBX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc; font-size: 1.2rem;'>El Pasaporte Oficial del Boxeo</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    modo = st.radio("Acceso", ["Iniciar Sesión", "Crear Pasaporte"], horizontal=True, label_visibility="collapsed")
    st.session_state.auth_mode = modo
    
    with st.container(border=True):
        if modo == "Iniciar Sesión":
            st.subheader("Entrar al Ring")
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            if st.button("INICIAR SESIÓN", type="primary"):
                success, data = database.authenticate_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = data
                    st.success("¡Bienvenido, campeón!")
                    st.rerun()
                else:
                    st.error("❌ " + data)
        else:
            st.subheader("Crear Pasaporte de Peleador")
            col1, col2 = st.columns(2)
            with col1: nombre = st.text_input("Nombre")
            with col2: apellido = st.text_input("Apellido")
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            gym_origen = st.selectbox("¿Cuál es tu esquina (Sede)?", ["Rounds x Best Training", "Rounds x CrossFit Company"])
            codigo_staff = st.text_input("Código de Staff (Solo Entrenadores)", type="password", help="Si eres alumno, deja este campo vacío.")
            
            if st.button("REGISTRARME", type="primary"):
                success, msg = database.register_user(nombre, apellido, email, password, gym_origen, codigo_staff)
                if success:
                    st.success("✅ " + msg + ". Redirigiendo al login...")
                    st.session_state.auth_mode = "Iniciar Sesión"
                    st.rerun() # Fuerza la recarga para mandarlo a Iniciar Sesión automáticamente

# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
def render_dashboard():
    user = st.session_state.user_data
    
    col_logo, col_settings = st.columns([4, 1])
    with col_logo:
        st.markdown("<h2 style='color:#d11124; margin:0; font-size: 2.5rem;'>ROUNDS BY CBX</h2>", unsafe_allow_html=True)
        if user.get('rol') == 'pro':
            st.markdown("<span style='background-color:#FFD700; color:black; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:0.8rem;'>👑 PROMOTOR (PRO - $5/mes)</span>", unsafe_allow_html=True)
        elif user.get('rol') == 'member':
            st.markdown("<span style='background-color:#d11124; color:white; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:0.8rem;'>🥊 PELEADOR AFILIADO (Socio)</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='background-color:#555; color:white; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:0.8rem;'>🎒 PELEADOR AMATEUR (Free)</span>", unsafe_allow_html=True)

    with col_settings:
        with st.popover("⚙️ AJUSTES", use_container_width=True):
            st.markdown("<h4 style='color:#d11124; margin-bottom:0;'>MI PASAPORTE</h4>", unsafe_allow_html=True)
            
            # Selector de Avatares Premium (A prueba de móviles)
            st.markdown("📸 **Avatar de Peleador**")
            avatar_opts = {
                "Predeterminado": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
                "Tyson Vibe": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=200",
                "Ali Vibe": "https://images.unsplash.com/photo-1509255929945-586a420363aa?q=80&w=200",
                "Rocky Vibe": "https://images.unsplash.com/photo-1614312674483-36526eb6dfdc?q=80&w=200"
            }
            sel_av = st.selectbox("Elige tu estilo:", list(avatar_opts.keys()), label_visibility="collapsed")
            if st.button("Guardar Avatar"):
                st.session_state.user_avatar = avatar_opts[sel_av]
                st.success("Actualizado")
                st.rerun()
                
            st.button("💳 Conectar Billetera Web3 (Fase 2)", use_container_width=True)
            st.markdown("---")
            if st.button("🔴 Cerrar Sesión", key="logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_data = None
                st.rerun()

    tabs_list = ["👤 PASAPORTE", "🥊 ACTIVIDADES", "📚 ALMANAQUE"]
    if user.get('rol') == 'coach':
        tabs_list.insert(1, "📋 DASHBOARD COACH")
        
    tabs = st.tabs(tabs_list)
    
    tab_perfil = tabs[0]
    if user.get('rol') == 'coach':
        tab_coach = tabs[1]
        tab_actividades = tabs[2]
        tab_almanaque = tabs[3]
    else:
        tab_actividades = tabs[1]
        tab_almanaque = tabs[2]
        
    # ------------------ TAB: PERFIL (PASSPORT) ------------------
    with tab_perfil:
        xp = user.get('xp', 0)
        nivel = (xp // 100) + 1
        xp_next = nivel * 100
        progreso_xp = (xp % 100)
        # Temporada y Avatar dinámica
        import base64
        import pytz
        from datetime import datetime
        
        tz_ecuador = pytz.timezone('America/Guayaquil')
        ahora = datetime.now(tz_ecuador)
        fin_de_ano = tz_ecuador.localize(datetime(2026, 12, 31, 23, 59, 59))
        dias_restantes = (fin_de_ano - ahora).days
        sesiones_hechas = st.session_state.get("entrenamientos_completados", 0)
        
        col_pass1, col_pass2 = st.columns([3, 1])
        with col_pass1:
            st.markdown("### 🗓️ TEMPORADA 2026")
            st.markdown(f"<p style='color:#FFD700; font-size:1.1rem; margin-bottom:0;'>{ahora.strftime('%d de %b, %Y | %H:%M')} (EC)</p>", unsafe_allow_html=True)
            st.caption(f"⏳ Faltan {dias_restantes} días para el cierre | Sesiones Registradas: {sesiones_hechas}")
            
        with col_pass2:
            with st.popover("📷 Tomar Foto"):
                foto_camara = st.camera_input("Sonríe al lente")
                if foto_camara is not None:
                    base64_img = base64.b64encode(foto_camara.getvalue()).decode()
                    st.session_state.user_avatar = f"data:image/jpeg;base64,{base64_img}"
                    # Guardaríamos en SQLite aquí
                    st.success("Foto guardada con éxito.")
                    st.rerun()

        avatar_img = st.session_state.get('user_avatar', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
        
        st.markdown(f"""
        <div class="passport-card">
            <h2 style='margin-top:0; color:#d11124;'>RÉCORD DE PELEADOR</h2>
            <hr style='border-color:#444;'>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="{avatar_img}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #d11124; box-shadow: 0 0 10px rgba(209,17,36,0.5);">
                    <div>
                        <h1 style="margin: 0; font-size: 2.5rem;">{user['nombre'].upper()} {user['apellido'].upper()}</h1>
                        <p style="color: #aaa; margin: 0; font-size: 1.1rem;">Esquina: {user['gym_origen']}</p>
                    </div>
                </div>
                <div style="text-align: right; background: rgba(0,0,0,0.5); padding: 10px 20px; border-radius: 8px; border: 1px solid #333;">
                    <h2 style="margin: 0; color: #FFD700; font-size: 2rem;">NIVEL {nivel}</h2>
                    <small style="color: #ccc;">{xp} / {xp_next} XP</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progreso_xp / 100.0, text="Progreso al siguiente nivel")
        
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            st.info(f"**TÍTULO:** {'Amateur' if nivel < 5 else 'Profesional'}")
            st.warning(f"**BOLSA ACTUAL:** {user['cbx_coins']} CBX Coins 🪙")
        with col_stats2:
            st.success("**MEMBRESÍA:** " + ("Activa (Pro)" if user['rol'] == 'pro' else "Socio de Gym" if user['rol'] == 'member' else "Amateur (Gratuita)"))
            
        # NUEVO SISTEMA: GIMNASIO / PLAN PRO
        st.markdown("### 🏆 Beneficios y Planes")
        with st.container(border=True):
            if user['rol'] == 'pro':
                st.success("✅ Eres usuario PRO. Tienes acceso total a las Comunidades y Descuentos.")
            else:
                col_plan1, col_plan2 = st.columns(2)
                with col_plan1:
                    st.markdown("**Plan PRO Estándar:** $5.99/mes")
                    st.button("Mejorar a PRO")
                with col_plan2:
                    st.markdown("**Descuento para Socios (Gym Rounds):** $2.50/mes")
                    st.button("Verificar Membresía Gym")
                    
        # INICIALIZACIÓN DE VARIABLES
        if "entrenamientos_completados" not in st.session_state: 
            st.session_state.entrenamientos_completados = 0
            
        # REGISTRO DE SESIÓN DEL DÍA
        st.markdown("---")
        st.markdown("### 📋 Sesión del Día")
        st.info("Registra tu asistencia y tu estado físico/emocional después de entrenar en tu sede.")
        
        with st.container(border=True):
            st.markdown("#### 1. Evaluación Física y Emocional (Wellness Check-in)")
            mood_opts = ["Alegre", "Eufórico", "Relajado", "Motivado", "Neutral", "Cansado", "Agotado", "Frustrado", "Desanimado", "Estresado"]
            st.selectbox("🧠 Estado de Ánimo Principal", mood_opts)
            
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                st.slider("🔋 Nivel de Energía", 1, 5, 3)
                st.slider("❤️ Nivel de Recuperación", 1, 5, 3)
            with col_w2:
                st.slider("📉 Nivel de Fatiga", 1, 5, 3)
                st.slider("🔥 Nivel de Motivación", 1, 5, 4)
                
            gap_opts = ["Nada, me siento bien", "Jab", "Cross", "Hook", "Defensa", "Footwork", "Combinaciones", "Condición física", "Técnica", "Sparring", "Otro"]
            st.selectbox("¿Qué sentiste que te faltó aprender o mejorar hoy?", gap_opts)
            
            st.markdown("#### 2. Confirmación de Asistencia")
            if st.button("MARCAR SESIÓN COMO COMPLETADA 🥊", use_container_width=True, type="primary"):
                st.session_state.entrenamientos_completados += 1
                st.toast("🥊 ¡Sesión registrada con éxito! El coach ha recibido tus estadísticas.")
                st.success(f"¡Has sumado una nueva sesión! (Sesión #{st.session_state.entrenamientos_completados} del año).")

        # Dashboard de Analíticas de Usuario
        if st.session_state.entrenamientos_completados > 0:
            st.markdown("---")
            st.markdown("<h3 style='color:#FFD700;'>📊 ESTADÍSTICAS TEMPORADA 2026</h3>", unsafe_allow_html=True)
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                st.metric(label="✅ Sesiones (Año)", value=f"{st.session_state.entrenamientos_completados}", delta="¡Buen ritmo!")
            with col_a2:
                st.metric(label="💪 Motivación Promedio", value="4.2 / 5", delta="Alta")

    # ------------------ TAB: DASHBOARD COACH (Solo para Entrenadores) ------------------
    if user.get('rol') == 'coach':
        with tab_coach:
            st.header("📊 Tablero del Entrenador")
            st.markdown(f"<p style='color:#ccc;'>Analíticas de bienestar exclusivas de tu sede: <b>{user['gym_origen']}</b>.</p>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(f"### Estado General: {user['gym_origen']}")
                col_c1, col_c2, col_c3 = st.columns(3)
                col_c1.metric("Ánimo", "72%", "+5%")
                col_c2.metric("Fatiga", "68%", "-2%")
                col_c3.metric("Recuperación", "75%", "+10%")
                st.info("Insight: Muchos alumnos en tu sede sienten que necesitan mejorar defensa esta semana.")
                
            st.markdown("---")
            with st.expander("🌍 Liga de Sedes (Acceso Global)"):
                st.write("Visualiza el rendimiento de otras sedes (Rounds x Best Training vs Rounds x CrossFit Company).")
                clave = st.text_input("Clave de Mando Global", type="password")
                if clave == "ADMIN2026":
                    st.success("Acceso concedido.")
                    col_g1, col_g2 = st.columns(2)
                    with col_g1:
                        st.markdown("**Rounds x Best Training**")
                        st.metric("Asistencia Global", "1,240 Sesiones", "1° Lugar")
                        st.metric("Motivación Promedio", "4.5 / 5")
                    with col_g2:
                        st.markdown("**Rounds x CrossFit Company**")
                        st.metric("Asistencia Global", "980 Sesiones", "2° Lugar")
                        st.metric("Motivación Promedio", "4.1 / 5")
                    st.info("💡 Al final del año, puedes liberar estas métricas para fomentar la competencia sana entre alumnos de distintas sedes.")

    # ------------------ TAB: ACTIVIDADES (GRUPO) ------------------
    with tab_actividades:
        st.header(f"Ring de la Sede: {user['gym_origen']}")
        st.markdown("<p style='color:#ccc;'>Chat Grupal: Misiones y comunicados oficiales de tu entrenador.</p>", unsafe_allow_html=True)
        
        if user.get('rol') == 'coach':
            with st.expander(f"📝 Transmitir mensaje a todos en {user['gym_origen']}", expanded=True):
                msj = st.text_area("Mensaje para la clase (Ej. WOD, recordatorios):")
                if st.button("Publicar en el Ring"):
                    st.success(f"Actividad publicada exitosamente a los alumnos de {user['gym_origen']}.")
                    
        st.markdown("### Septiembre 2026")
        
        with st.chat_message("coach", avatar="🥊"):
            st.markdown("**COACH ESTEFANO**")
            st.write("Chicos, esta semana vamos a trabajar más defensa y movilidad. Recuerden practicar su jab-cross en casa.")
            st.caption("Hace 2 horas")
            col_b1, col_b2, col_b3 = st.columns([1,1,2])
            with col_b1:
                if st.button("Aprobar ✅", key="apr1"): st.toast("Has aprobado la actividad.")
            with col_b2:
                if st.button("Duda ❓", key="duda1"): st.toast("Notificado al coach.")
            
        with st.chat_message("coach", avatar="🥊"):
            st.markdown("**COACH ESTEFANO**")
            st.write("El sábado tendremos sesión especial de Sparring. 10:00 AM. Traigan cabezal y bucal obligatorio.")
            st.caption("Hace 1 día")
            col_b1, col_b2, col_b3 = st.columns([1,1,2])
            with col_b1:
                if st.button("Aprobar ✅", key="apr2"): st.toast("Has aprobado la actividad.")
            with col_b2:
                if st.button("Duda ❓", key="duda2"): st.toast("Notificado al coach.")

    # ------------------ TAB: ALMANAQUE ------------------
    with tab_almanaque:
        st.header("📚 Almanaque de Boxeo")
        st.markdown("<p style='color:#ccc;'>Archivo histórico y biblioteca técnica de Rounds.</p>", unsafe_allow_html=True)
        
        st.subheader("Técnicas Básicas (Drop 1)")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            with st.container(border=True):
                st.markdown("### 1. El Jab")
                st.write("Golpe recto con la mano adelantada. Fundamento de la distancia.")
                st.button("Ver Estudio Mecánico", key="tec1")
        with col_t2:
            with st.container(border=True):
                st.markdown("### 2. El Cross (Recto)")
                st.write("Golpe de poder con la mano atrasada. Rotación de cadera clave.")
                st.button("Ver Estudio Mecánico", key="tec2")
                
        st.markdown("---")
        st.subheader("Peleas Históricas del Mes")
        with st.container(border=True):
            st.markdown("### Ali vs Frazier I (La Pelea del Siglo)")
            st.caption("8 de Marzo, 1971 | Madison Square Garden")
            st.write("La primera batalla épica entre dos campeones invictos. Un choque de estilos y personalidades que definió una era.")



if __name__ == "__main__":
    if st.session_state.logged_in and st.session_state.user_data:
        render_dashboard()
    else:
        render_auth()
