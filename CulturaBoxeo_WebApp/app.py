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
            gym_origen = st.selectbox("¿Cuál es tu esquina (Sede)?", ["Independiente (Sin Gym)", "Rounds CBX (Matriz)", "Best Training", "CrossFit Company"])
            
            if st.button("REGISTRARME", type="primary"):
                success, msg = database.register_user(nombre, apellido, email, password, gym_origen)
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

    tab_perfil, tab_entrenamientos, tab_noticias = st.tabs([
        "👤 PASAPORTE", "🥊 ACADEMIA & WOD", "📰 NOTICIAS"
    ])
    
    # ------------------ TAB: PERFIL (RÉCORD DE PELEADOR) ------------------
    with tab_perfil:
        xp = user.get('xp', 0)
        nivel = (xp // 100) + 1
        xp_next = nivel * 100
        progreso_xp = (xp % 100)
        
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
                    
        # NUEVO SISTEMA: ACTIVIDADES DEL COACH
        st.markdown("---")
        st.markdown("### 📋 Entrenamiento del Día (Asignado)")
        st.info(f"Tu esquina **{user['gym_origen']}** te ha asignado la siguiente misión para hoy:")
        with st.container(border=True):
            st.markdown("**🔥 Circuito de Resistencia (Semana 1)**")
            st.markdown("- 3 Rounds de Sombra (Calentamiento)\n- 5 Rounds de Costal Pesado (Enfoque en combinaciones 1-2-3)\n- 100 Sentadillas libres")
            if st.button("Marcar como completado ✅", use_container_width=True):
                st.balloons()
                st.success("¡Misión cumplida! Coach notificado.")
                    
        # SISTEMA DE ENTRENAMIENTO ESTILO FIGHTCAMP / PUNCHLAB
        st.markdown("### 📈 Bitácora de Entrenamiento (Hoy)")
        st.markdown("<p style='color:#ccc;'>Registra tu sesión de hoy. Tu entrenador podrá validar estos datos en tu pasaporte.</p>", unsafe_allow_html=True)
        
        # Inicializar métricas en session_state para simular la persistencia
        if "entrenamientos_completados" not in st.session_state: st.session_state.entrenamientos_completados = 0
        if "punch_volume_total" not in st.session_state: st.session_state.punch_volume_total = 0
        if "racha_dias" not in st.session_state: st.session_state.racha_dias = 0

        with st.expander("📝 Cargar Informe de Sesión Hoy", expanded=True):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                tiempo_entrenamiento = st.number_input("⏱️ Tiempo de entrenamiento (minutos)", min_value=15, max_value=120, value=60, step=5)
                enfoque = st.multiselect("🎯 Enfoque Principal", ["Sombra", "Costal pesado", "Mitts/Gobernadoras", "Sparring", "Físico"], default=["Sombra"])
            with col_m2:
                intensidad = st.slider("🔥 Intensidad Percibida (1-10)", 1, 10, 7)
                st.caption("1 = Paseo en el parque | 10 = Nivel Campeonato")

            if st.button("Guardar Entrenamiento del Día", type="primary"):
                # Simular cálculo avanzado (Punch Volume Estimado = minutos * intensidad * factor)
                factor_boxeo = 20 if ("Costal pesado" in enfoque or "Mitts/Gobernadoras" in enfoque) else 10
                volumen_estimado = int(tiempo_entrenamiento * (intensidad/10.0) * factor_boxeo)
                
                st.session_state.entrenamientos_completados += 1
                st.session_state.punch_volume_total += volumen_estimado
                st.session_state.racha_dias += 1
                recompensa = 50 * st.session_state.racha_dias
                st.session_state.user_data['cbx_coins'] += recompensa
                
                st.success(f"¡Sesión Guardada! Has lanzado un estimado de **{volumen_estimado} golpes** (Output). Ganaste {recompensa} CBX.")
                st.rerun()

        # Dashboard de Analíticas de Usuario
        if st.session_state.entrenamientos_completados > 0:
            st.markdown("---")
            st.markdown("<h3 style='color:#FFD700;'>📊 MIS ESTADÍSTICAS (GYM ANALYTICS)</h3>", unsafe_allow_html=True)
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.metric(label="🔥 Racha Actual", value=f"{st.session_state.racha_dias} Días", delta="¡Sigue así!")
            with col_a2:
                st.metric(label="🥊 Punch Volume (Est.)", value=f"{st.session_state.punch_volume_total}", delta="+ Poder")
            with col_a3:
                st.metric(label="✅ Sesiones (Mes)", value=f"{st.session_state.entrenamientos_completados}", delta="Registradas")

    # ------------------ TAB: ENTRENAMIENTOS ------------------
    with tab_entrenamientos:
        st.header("Academia de Combate")
        st.markdown("<p style='color:#ccc;'>Estructuras de aprendizaje paso a paso. Únete a los próximos drops.</p>", unsafe_allow_html=True)
        
        for ruta, niveles in ACADEMIA_DB.items():
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
                            st.info(f"⏳ **PRÓXIMO DROP:** Disponible {t.get('fecha_drop', 'Próximamente')}. ¡Mantente atento a la comunidad!")
                        else:
                            st.info(t['instrucciones'])
                            st.video(t['video_url'])
                    else:
                        st.error(f"🔒 Contenido exclusivo. Requiere membresía AFILIADO o PRO.")
                    st.markdown("---")

    # ------------------ TAB: NOTICIAS ------------------
    with tab_noticias:
        if st.session_state.view_noticia is None:
            st.header("Última Hora (Live)")
            
            # Anuncio Periodístico Interactivo
            st.markdown("""
            <div style='background-color: rgba(26,26,26,0.9); padding: 15px; border-left: 5px solid #d11124; margin-bottom: 20px;'>
                <h3 style='color: white; margin-top:0;'>LA COMUNICACIÓN TIENE QUE EVOLUCIONAR.</h3>
                <p style='color: #ccc; font-style: italic;'>
                El periodismo deportivo ha estado estático por décadas. Prepárate para la primera plataforma de noticias verdaderamente interactiva. Convierte la lectura en acción: debate y especula en nuestros mercados.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            import agente_noticias
            
            @st.cache_data(ttl=7200) # Se actualiza cada 2 horas automáticamente
            def get_live_news():
                return agente_noticias.fetch_live_news()
                
            noticias_vivo = get_live_news()
            
            # Fallback en caso de que el scraper falle (sin internet)
            if not noticias_vivo:
                import mock_data
                noticias_vivo = mock_data.NOTICIAS
            
            for n in noticias_vivo:
                # Filtrar imagenes rotas o URLs extrañas
                img_url = n.get('imagen_url', '')
                if not img_url or "http" not in str(img_url):
                    img_url = "https://images.unsplash.com/photo-1599552375246-24ee029302e3?q=80&w=800"
                
                with st.container(border=True):
                    try:
                        st.image(img_url, use_column_width=True)
                    except:
                        # Si Streamlit no puede procesar la imagen remotamente, usa un hard-fallback seguro
                        img_url = "https://images.unsplash.com/photo-1599552375246-24ee029302e3?q=80&w=800"
                        st.image(img_url, use_column_width=True)
                        
                    st.markdown(f"<h3 style='color:white; margin-bottom:0;'>{n['titulo']}</h3>", unsafe_allow_html=True)
                    st.caption(f"📰 **{n['fuente'].upper()}** | 🕒 {n['fecha']}")
                    
                    col_leer, col_link = st.columns(2)
                    with col_leer:
                        if st.button(f"Leer Artículo", key=f"btn_leer_{n['id']}", use_container_width=True):
                            n['imagen_url'] = img_url
                            st.session_state.view_noticia = n
                            st.rerun()
                    with col_link:
                        st.link_button("Noticia Original ↗", url=n.get('link', '#'), use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            n = st.session_state.view_noticia
            if st.button("← Volver al Feed de Noticias", type="secondary"):
                st.session_state.view_noticia = None
                st.rerun()
            
            # Formato de Artículo Premium (Estilo Netflix / NYT)
            st.markdown(f"""
            <div style="width: 100%; height: 400px; background-image: url('{n['imagen_url']}'); background-size: cover; background-position: center; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);"></div>
            <h1 style='font-size: 3rem; line-height: 1.1; margin-bottom: 10px; color: #fff;'>{n['titulo']}</h1>
            <h3 style='color: #aaa; font-family: sans-serif; font-weight: normal; margin-top: 0;'>{n.get('subtitulo', '')}</h3>
            <p style='color: #d11124; font-weight: bold;'>{n['fecha']} | REDACCIÓN: {n['fuente']}</p>
            <hr style='border-color: #333;'>
            """, unsafe_allow_html=True)
            
            # Contenido (Simulando un artículo largo y rico de IA)
            st.markdown(f"<div style='font-size: 1.2rem; line-height: 1.8; color: #eee; text-align: justify;'>{n['contenido_html']}</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("📰 Leer fuente original completa", url=n.get('link', '#'), type="secondary")
            
            st.markdown("---")
            st.markdown("<div style='text-align: right; color: #aaa; font-style: italic;'>Una exclusiva de <b>JP Vanguard Media Group</b></div>", unsafe_allow_html=True)
            
            # Eliminado mercado de especulación para enfocar en entrenamiento



if __name__ == "__main__":
    if st.session_state.logged_in and st.session_state.user_data:
        render_dashboard()
    else:
        render_auth()
