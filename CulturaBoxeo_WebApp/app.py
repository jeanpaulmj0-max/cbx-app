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
    
    /* Animación 10x y Fondo de Cine de Boxeo (Gritty/Vintage con overlay oscuro) */
    .stApp {
        background: linear-gradient(rgba(15, 10, 10, 0.85), rgba(25, 5, 5, 0.95)), url('https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?q=80&w=2000') no-repeat center center fixed !important;
        background-size: cover !important;
    }
    
    html, body, p, div, span, label, input, li { font-family: 'Oswald', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 1px; color: #ffffff;}
    .stButton>button {
        width: 100%; border-radius: 4px; font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.2rem; background-color: #d11124; color: white; border: none;
    }
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
        padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DATOS POR DEFECTO (A PRUEBA DE FALLOS MVP)
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
    st.markdown("<h1 style='text-align: center; color: #d11124; font-size: 4.5rem; text-shadow: 2px 2px 4px #000;'>ROUNDS BY CBX</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #aaa;'>FIGHT PASSPORT - ACCESO DIGITAL</h4><hr style='border-color:#444;'>", unsafe_allow_html=True)
    
    # Usamos session_state para controlar qué vista mostrar si recién se registró
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Iniciar Sesión"
        
    modo = st.radio("Acceso", ["Iniciar Sesión", "Registrar Pasaporte"], horizontal=True, index=0 if st.session_state.auth_mode == "Iniciar Sesión" else 1)
    st.session_state.auth_mode = modo
    
    if modo == "Iniciar Sesión":
        with st.form("login_form"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            submit_login = st.form_submit_button("ENTRAR AL RING")
            
        if submit_login:
            if not email.strip() or not password.strip():
                st.error("⚠️ Por favor, llena tu correo y contraseña.")
            else:
                success, data = database.authenticate_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = data
                    st.rerun()
                else:
                    st.error("❌ " + data) # Correo o contraseña incorrectos
                
    else:
        with st.form("registro_form"):
            nombre = st.text_input("Nombre *")
            apellido = st.text_input("Apellido *")
            email = st.text_input("Correo electrónico *")
            password = st.text_input("Contraseña (mínimo 6 caracteres) *", type="password")
            password_conf = st.text_input("Confirmar Contraseña *", type="password")
            gym_origen = st.selectbox("Sede / Afiliación", ["Independiente (Free)", "Rounds CBX por Best Training", "Rounds CBX por CrossFit Company"])
            
            submit_reg = st.form_submit_button("CREAR PASAPORTE")
            
        if submit_reg:
            if not all([nombre.strip(), apellido.strip(), email.strip(), password.strip(), password_conf.strip()]):
                st.error("⚠️ Tienes que llenar absolutamente TODOS los campos marcados con *.")
            elif password != password_conf:
                st.error("⚠️ Las contraseñas no coinciden. Escríbelas de nuevo.")
            else:
                success, msg = database.register_user(nombre, apellido, email, password, gym_origen)
                if success:
                    st.success("✅ " + msg + ". Redirigiendo al login...")
                    st.session_state.auth_mode = "Iniciar Sesión"
                    st.rerun() # Fuerza la recarga para mandarlo a Iniciar Sesión automáticamente
                else:
                    st.error("❌ " + msg)

# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
def render_dashboard():
    user = st.session_state.user_data
    
    col_logo, col_settings = st.columns([4, 1])
    with col_logo:
        st.markdown("<h2 style='color:#d11124; margin:0; font-size: 2.5rem;'>ROUNDS BY CBX</h2>", unsafe_allow_html=True)
        # ------------------ SISTEMA DE NIVELES (Estilo Gemini) ------------------
        if user.get('rol') == 'pro':
            st.markdown("<span style='background-color:#FFD700; color:black; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:0.8rem;'>👑 PROMOTOR (PRO - $5/mes)</span>", unsafe_allow_html=True)
        elif user.get('rol') == 'member':
            st.markdown("<span style='background-color:#d11124; color:white; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:0.8rem;'>🥊 PELEADOR AFILIADO (Socio)</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='background-color:#555; color:white; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:0.8rem;'>🎒 PELEADOR AMATEUR (Free)</span>", unsafe_allow_html=True)

    with col_settings:
        with st.popover("⚙️ AJUSTES Y HERRAMIENTAS", use_container_width=True):
            st.markdown("<h4 style='color:#d11124; margin-bottom:0;'>MI PASAPORTE</h4>", unsafe_allow_html=True)
            
            # Botón / Uploader de Foto
            foto_up = st.file_uploader("📸 Cargar Foto de Perfil (Avatar)", type=['jpg','png','jpeg'], label_visibility="collapsed")
            if foto_up is not None:
                import base64
                base64_img = base64.b64encode(foto_up.getvalue()).decode()
                st.session_state.user_avatar = f"data:image/png;base64,{base64_img}"
                st.success("Avatar actualizado")
                
            st.button("💳 Conectar Billetera Web3 (Fase 2)", use_container_width=True)
            st.markdown("---")
            if st.button("🔴 Cerrar Sesión", key="logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_data = None
                st.rerun()

    tab_perfil, tab_comunidad, tab_entrenamientos, tab_noticias, tab_fantasy, tab_tienda = st.tabs([
        "👤 RÉCORD", "💬 EL RING", "🥊 ACADEMIA", "📰 NOTICIAS", "🎯 FANTASY", "🛒 TIENDA"
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
            
        st.markdown("### 🚀 Acelera tu carrera (Red de Contactos)")
        with st.expander("🤝 Programa de Referidos (Invita y Gana)"):
            st.markdown("El boxeo es un deporte de equipos. Invita a tu esquina y gana monedas para apostar o canjear por descuentos reales.")
            st.code(f"https://cbx-app.streamlit.app/?ref={user['nombre'][:3].upper()}{str(user.get('id', '000'))}", language="text")
            if st.button("Copiar Link y Ganar 500 CBX por amigo"):
                st.toast("Link copiado al portapapeles. ¡Mándalo por WhatsApp!", icon="🔗")
                
        with st.expander("📍 Valida tu ciudad para un nuevo Gym ROUNDS"):
            st.markdown("¿Quieres que abramos una sede de **ROUNDS CBX** en tu zona? Sé el fundador de tu comunidad.")
            ciudad = st.text_input("Ingresa tu ciudad / sector:")
            if st.button("Solicitar Sede Oficial"):
                if ciudad:
                    st.success(f"Voto registrado para {ciudad}. Si juntamos 100 peticiones, vamos para allá. Has ganado 100 CBX por tu voto.")
                    st.session_state.user_data['cbx_coins'] += 100
                else:
                    st.error("Escribe tu ciudad.")

    # ------------------ TAB: COMUNIDAD ------------------
    with tab_comunidad:
        st.header("El Ring - Comunidad Global")
        st.markdown("<p style='color:#ccc;'>El cruce perfecto entre el Boxeo Profesional, el Cine, y la Cultura Urbana.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            nuevo_post = st.text_area("Nuevo Post", placeholder="¿Qué tienes en mente, campeón? Comparte debates, análisis o fotos...", label_visibility="collapsed")
            
            # Gadgets tipo Twitter/Threads
            col_t1, col_t2, col_t3, col_t4, col_btn = st.columns([1,1,1,1,3])
            with col_t1: st.button("📷 Foto", use_container_width=True)
            with col_t2: st.button("🎞️ GIF", use_container_width=True)
            with col_t3: st.button("📊 Encuesta", use_container_width=True)
            with col_t4: st.button("📍 Lugar", use_container_width=True)
            with col_btn:
                btn_publicar = st.button("PUBLICAR", use_container_width=True, type="primary")

        if btn_publicar:
            if nuevo_post.strip():
                st.session_state.comunidad_posts.insert(0, {
                    "id": f"C{len(st.session_state.comunidad_posts)+1}",
                    "autor": f"{user['nombre']}_{user['apellido'][0]}",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "contenido": f"{nuevo_post}"
                })
                
                # Sistema de Incentivos (Gamificación)
                if "posts_count" not in st.session_state:
                    st.session_state.posts_count = 0
                st.session_state.posts_count += 1
                
                if st.session_state.posts_count == 2:
                    st.session_state.user_data['cbx_coins'] += 1000
                    st.balloons()
                    st.success("🎉 ¡RECOMPENSA DESBLOQUEADA! Has ganado 1,000 CBX Coins por tus primeras interacciones. Úsalas para obtener descuentos en la Tienda.")
                elif st.session_state.posts_count == 10:
                    st.session_state.user_data['cbx_coins'] += 5000
                    st.balloons()
                    st.success("🔥 ¡VETERANO DEL RING! Has ganado 5,000 CBX Coins. Puedes usarlas para desbloquear equipo premium con descuento.")
                else:
                    st.success(f"Publicado en El Ring. (Post #{st.session_state.posts_count})")
                    
                st.rerun()
            else:
                st.warning("Escribe algo antes de publicar.")
                
        st.markdown("---")
        for post in st.session_state.comunidad_posts:
            st.markdown(f"""
            <div class='post-card' style='color: white;'>
                <small style='color:#d11124;'><b>@{post['autor']}</b> • {post['fecha']}</small>
                <p style='margin-top:5px; color: white;'>{post['contenido']}</p>
            </div>
            """, unsafe_allow_html=True)

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
                # Asegurar fallback de imagen si la noticia no trajo una
                img_bg = n.get('imagen_url')
                if not img_bg:
                    img_bg = "https://images.unsplash.com/photo-1599552375246-24ee029302e3?q=80&w=800"
                    
                tarjeta_html = f"""<div style="position: relative; width: 100%; height: 380px; border-radius: 8px; overflow: hidden; margin-bottom: 10px; background-image: url('{img_bg}'); background-size: cover; background-position: top center; border: 1px solid #333;"><div style="position: absolute; bottom: 0; left: 0; right: 0; height: 70%; background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0) 100%);"></div><div style="position: absolute; top: 15px; left: 15px; color: white; font-size: 0.7rem; font-weight: bold; letter-spacing: 2px; text-shadow: 1px 1px 2px #000;">ROUNDS BY CBX</div><div style="position: absolute; top: 15px; right: 15px; color: #fff; font-size: 0.65rem; font-weight: bold; background: rgba(209,17,36,0.8); padding: 4px 10px; border-radius: 20px; border: 1px solid #555;">{n['fuente'].upper()}</div><div style="position: absolute; bottom: 20px; left: 20px; right: 20px;"><h2 style="color: white; margin: 0; line-height: 1.1; font-size: 2.2rem; text-transform: uppercase; text-shadow: 2px 2px 4px #000;">{n['titulo']}</h2><div style="height: 3px; width: 50px; background-color: #d11124; margin: 12px 0;"></div><small style="color: #ccc; font-size: 0.8rem;">{n['fecha']}</small></div></div>"""
                st.markdown(tarjeta_html, unsafe_allow_html=True)
                
                if st.button(f"Leer Artículo", key=f"btn_leer_{n['id']}"):
                    n['imagen_url'] = img_bg # Actualizar el objeto con la imagen fallback
                    st.session_state.view_noticia = n
                    st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
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
            
            st.markdown("---")
            st.markdown("<div style='text-align: right; color: #aaa; font-style: italic;'>Una exclusiva de <b>JP Vanguard Media Group</b></div>", unsafe_allow_html=True)
            
            # Mercado de Predicción Interactivo
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("<h4 style='color: #FFD700; margin-top:0;'>📊 MERCADO DE ESPECULACIÓN</h4>", unsafe_allow_html=True)
                st.markdown(f"¿Qué crees que pasará respecto a esta noticia? Haz tu predicción y gana CBX Coins.")
                
                col_y, col_n = st.columns(2)
                with col_y:
                    if st.button("SÍ, SUCEDERÁ (Cuota x2.5)"):
                        st.toast("Especulación registrada.", icon="📈")
                with col_n:
                    if st.button("NO SUCEDERÁ (Cuota x1.3)"):
                        st.toast("Especulación registrada.", icon="📉")

    # ------------------ TAB: FANTASY ------------------
    with tab_fantasy:
        st.header("Casino Digital - Fantasy Picks")
        
        st.info("💡 **VISIÓN EARLY ADOPTERS:** En este momento estamos validando un producto que en un futuro te permitirá **ganar dinero real**. Los usuarios más fieles que participen en esta fase Beta tendrán beneficios económicos exclusivos en la siguiente etapa.")
        
        with st.expander("🏆 ¿CÓMO CANJEAR TUS CBX COINS AHORA?", expanded=True):
            st.markdown("""
            El dinero real lo usas en la Tienda. Tus CBX Coins sirven para desbloquear súper-descuentos y beneficios:
            *   🛒 **10,000 CBX:** Canjea por un cupón de 20% OFF en Guantes de Importación.
            *   🥊 **20,000 CBX:** Canjea por 1 Sesión de Entrenamiento (Rounds) gratis.
            *   💸 **Usuarios PRO:** Ganan un 15% adicional de descuento en toda la tienda automáticamente.
            """)
            
        col_bank, col_bets = st.columns(2)
        with col_bank:
            st.markdown(f"<div style='background:#111; padding:15px; border-radius:8px; border-left:4px solid #FFD700;'><h4>Bankroll:</h4><h2 style='color:#00ff00; margin:0;'>{user['cbx_coins']} CBX 🪙</h2></div>", unsafe_allow_html=True)
        with col_bets:
            st.markdown(f"<div style='background:#111; padding:15px; border-radius:8px; border-left:4px solid #d11124;'><h4>Apuestas Activas:</h4><h2 style='color:white; margin:0;'>{len(st.session_state.mis_apuestas)} 🎟️</h2></div>", unsafe_allow_html=True)
            
        if len(st.session_state.mis_apuestas) > 0:
            st.markdown("### 🎟️ Mis Boletas Activas")
            for b in st.session_state.mis_apuestas:
                st.markdown(f"""
                <div style='background:rgba(34,34,34,0.9); padding:10px; border-radius:5px; border-left:3px solid #00ff00; margin-bottom:5px;'>
                    <b>{b['pelea']}</b> | Pick: <span style='color:#FFD700;'>{b['pick']}</span> | Riesgo: {b['monto']} CBX | Pago Potencial: <b style='color:#00ff00;'>{b['retorno']:.2f} CBX</b>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Infraestructura de Comunidades de Especulación
        st.markdown("""
        <div style='background-color: rgba(34,34,34,0.9); padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #444;'>
            <h4 style='color: #FFD700; margin-top: 0;'>👑 Conviértete en Promotor de Fantasy</h4>
            <p style='color: #ccc; font-size: 0.9rem;'>
            ¿Quieres liderar tu propia comunidad? Los usuarios <b>PRO ($5/mes)</b> pueden crear sus propios "Mercados de Especulación" (Ej: <i>¿Peleará McGregor vs Topuria en 2027?</i>) e invitar a otros a apostar, llevándose una comisión de los premios.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("CREAR MI PROPIO MERCADO (Solo PRO)"):
            if user.get('rol') == 'pro':
                st.success("Acceso de Promotor concedido. El panel de creador de mercados se habilitará en la Fase 2.")
            else:
                st.error("🔒 Servicio Bloqueado: Exclusivo para PROMOTORES.")
                st.info("Mejora tu cuenta a PRO por solo $5.00/mes y obtén la licencia comercial para crear comunidades de especulación.")
        
        import mock_data
        for cart in mock_data.FANTASY_CARTELERAS:
            st.subheader(f"📅 {cart['titulo']}")
            for p in cart['combates']:
                with st.container(border=True):
                    st.markdown(f"<h4 style='text-align: center; margin-bottom: 0;'>🥊 {p['peleador_a']} <span style='color:#d11124;'>VS</span> {p['peleador_b']} 🥊</h4>", unsafe_allow_html=True)
                    
                    # Infraestructura tipo Casino (Boleta de Apuesta)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<div style='text-align:center; padding:10px; background:rgba(17,17,17,0.9); color:white; border-radius:5px;'><b>{p['peleador_a']}</b><br>🔥 Cuota: x{p['cuota_a']}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div style='text-align:center; padding:10px; background:rgba(17,17,17,0.9); color:white; border-radius:5px;'><b>{p['peleador_b']}</b><br>🔥 Cuota: x{p['cuota_b']}</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    col_bet1, col_bet2 = st.columns([2, 1])
                    with col_bet1:
                        monto = st.number_input("Monto a apostar (CBX Coins)", min_value=10, max_value=max(10, user['cbx_coins']), step=10, key=f"monto_{p['id']}")
                        seleccion = st.selectbox("Selecciona tu ganador", [p['peleador_a'], p['peleador_b']], key=f"sel_{p['id']}")
                    with col_bet2:
                        cuota_actual = p['cuota_a'] if seleccion == p['peleador_a'] else p['cuota_b']
                        retorno = monto * cuota_actual
                        st.markdown(f"<div style='text-align:center; margin-top:25px;'><small>Retorno Potencial:</small><br><b style='color:#00ff00; font-size:1.2rem;'>{retorno:.2f} CBX</b></div>", unsafe_allow_html=True)
                        if st.button("COLOCAR APUESTA", key=f"btn_bet_{p['id']}"):
                            if user['cbx_coins'] >= monto:
                                st.session_state.user_data['cbx_coins'] -= monto
                                st.session_state.mis_apuestas.append({
                                    "pelea": f"{p['peleador_a']} vs {p['peleador_b']}",
                                    "pick": seleccion,
                                    "monto": monto,
                                    "retorno": retorno
                                })
                                st.success(f"¡Boleta ingresada con éxito! Tu saldo restante es {st.session_state.user_data['cbx_coins']} CBX.")
                                st.rerun()
                            else:
                                st.error("Fondos insuficientes para esta apuesta.")

    # ------------------ TAB: TIENDA ------------------
    with tab_tienda:
        st.header("Mercado de Campeones")
        st.markdown(f"**Tu Saldo:** {user['cbx_coins']} CBX Coins 🪙")
        st.markdown("Equípate con lo mejor. Si tienes suficientes CBX Coins, solicita tu descuento al asesor en WhatsApp al hacer el pedido.")
        
        # UI Estilo E-Commerce Moderno
        tab_guantes, tab_sacos, tab_accesorios, tab_suplementos = st.tabs(["🥊 Guantes", "🏋️ Sacos e Implementos", "⚡ Accesorios", "💊 Suplementos"])
        
        def renderizar_categoria(categoria_filtro):
            import urllib.parse
            productos = [p for p in TIENDA_DB if p['categoria'] == categoria_filtro]
            col1, col2 = st.columns(2)
            for i, prod in enumerate(productos):
                with (col1 if i % 2 == 0 else col2):
                    tarjeta_producto = f"""
                    <div class="product-card">
                        <img src="{prod['img_url']}" class="product-img">
                        <div class="product-info">
                            <h4 style="margin: 0; color: white;">{prod['nombre']}</h4>
                            <p style="color: #aaa; font-size: 0.8rem; margin: 5px 0 10px 0;">{prod['desc']}</p>
                            <h3 style="color: #00ff00; margin: 0;">{prod['precio']}</h3>
                        </div>
                    </div>
                    """
                    st.markdown(tarjeta_producto, unsafe_allow_html=True)
                    
                    # Generar Link de WhatsApp
                    mensaje_ws = f"Hola, vengo de la app ROUNDS BY CBX. Me interesa comprar: {prod['nombre']} ({prod['precio']}). Mi usuario es: {user['nombre']} {user['apellido']}."
                    url_ws = f"https://wa.me/593998593226?text={urllib.parse.quote(mensaje_ws)}"
                    
                    st.link_button(f"Comprar vía WhatsApp", url=url_ws)
        
        with tab_guantes:
            renderizar_categoria("Guantes")
        with tab_sacos:
            renderizar_categoria("Sacos e Implementos")
        with tab_accesorios:
            renderizar_categoria("Artículos de Entrenamiento")
        with tab_suplementos:
            renderizar_categoria("Suplementos")

if __name__ == "__main__":
    if st.session_state.logged_in and st.session_state.user_data:
        render_dashboard()
    else:
        render_auth()
