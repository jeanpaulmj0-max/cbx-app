# mock_data.py
# Capa de datos para Cultura de Boxeo V1.0

ENTRENAMIENTOS = {
    "🔥 DROP 1: FUNDAMENTOS DEL STRIKING (Próximamente)": [
        {
            "id": "T01", "titulo": "Postura, Guardia y Desplazamiento", "nivel_orden": "Episodio 1",
            "descripcion": "La base de todo peleador. Aprende a pararte como un profesional y moverte sin cruzar las piernas.",
            "duracion": "10 min", "objetivo": "Técnica Base", "equipamiento": "Ninguno",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre",
            "instrucciones": "Mantén tu centro de gravedad bajo.",
            "acceso": "free"
        },
        {
            "id": "T02", "titulo": "Mecánica del Jab y Recto", "nivel_orden": "Episodio 2",
            "descripcion": "El 1-2. Cómo generar poder desde la cadera y no solo con los brazos.",
            "duracion": "15 min", "objetivo": "Precisión y Poder", "equipamiento": "Ninguno",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre",
            "instrucciones": "Gira el pie trasero al lanzar el recto.",
            "acceso": "free"
        }
    ],
    "🥊 RUTINAS CBX STUDIO (Exclusivo Socios)": [
        {
            "id": "T03", "titulo": "HIIT Boxeo: Sombra de Alta Intensidad", "nivel_orden": "Rutina 1",
            "descripcion": "Quema de calorías máxima simulando 3 rounds de campeonato.",
            "duracion": "20 min", "objetivo": "Cardio y Resistencia", "equipamiento": "Ninguno",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre",
            "instrucciones": "Sigue el ritmo del coach sin bajar la guardia.",
            "acceso": "member"
        },
        {
            "id": "T04", "titulo": "Destrucción de Costal", "nivel_orden": "Rutina 2",
            "descripcion": "Trabajo de potencia en el saco pesado enfocándose en ganchos al cuerpo.",
            "duracion": "30 min", "objetivo": "Potencia", "equipamiento": "Saco, Vendas, Guantes",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Desde el 14 de Septiembre",
            "instrucciones": "Asegúrate de vendar correctamente tus manos.",
            "acceso": "member"
        }
    ],
    "🛠️ CLINIC DE SPARRING (En Construcción)": [
        {
            "id": "T05", "titulo": "Gestión de Distancia y Tiempos", "nivel_orden": "Próximamente",
            "descripcion": "Módulo avanzado en desarrollo. Aprende a leer los tiempos de tu oponente.",
            "duracion": "-- min", "objetivo": "Sparring", "equipamiento": "Casco, Bucal, Guantes 16oz",
            "video_url": None, "estado": "construccion", "fecha_drop": "Próximamente",
            "instrucciones": "Módulo en grabación.",
            "acceso": "pro"
        }
    ]
}

NOTICIAS = [
    {
        "id": "n1",
        "titulo": "Nassourdine Imavov confirma que enfrentará a Sean Strickland por el título de UFC",
        "subtitulo": "El peso medio francés asegura que la pelea está firmada.",
        "fecha": "5 de Septiembre, 2026",
        "fuente": "El Rocktagono",
        "categoria": "UFC",
        "imagen_url": "https://images.unsplash.com/photo-1599552375246-24ee029302e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
        "contenido_html": "<p>En una reciente entrevista, Imavov dejó claro que los contratos ya están enviados. Nuestro modelo de extracción predice que el anuncio oficial se hará este fin de semana.</p><ul><li><b>Estatus:</b> Confirmación verbal</li><li><b>Sede probable:</b> Las Vegas</li></ul>"
    },
    {
        "id": "n2",
        "titulo": "UFC 309: El efecto dominó en el ranking Libra por Libra",
        "subtitulo": "Islam Makhachev busca la doble corona",
        "fecha": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "fuente": "MMA Fighting (Bot)",
        "categoria": "MMA / UFC",
        "imagen_url": "https://images.unsplash.com/photo-1544367567-0f2fcb0d9e0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "contenido_html": "<p>La victoria de este fin de semana podría consolidarlo como el #1 del mundo indiscutible. Sin embargo, Arman Tsarukyan ha prometido un final por nocaut en el primer round.</p><ul><li><b>Estatus:</b> Pelea confirmada</li><li><b>Relevancia:</b> Extrema</li></ul>"
    }
]

COMUNIDAD_POSTS_INICIALES = [
    {"id": "C1", "autor": "Coach_Juan", "fecha": "2026-09-01 08:30", "contenido": "¿Cuál es su combinación favorita para salir de las cuerdas? Yo prefiero el gancho de izquierda al hígado seguido de pivote."},
    {"id": "C2", "autor": "Laura_CBX", "fecha": "2026-08-31 19:15", "contenido": "Ayer completé la rutina 'Condicionamiento Espartano' de la app y casi no sobrevivo. ¡Excelente trabajo la sección de Entrenamientos!"}
]

FANTASY_CARTELERAS = [
    {
        "id": "F1", "titulo": "UFC 309: El Cierre de Año", "fecha": "2026-09-15",
        "combates": [
            {"id": "C1", "peleador_a": "Islam Makhachev", "peleador_b": "Arman Tsarukyan", "cuota_a": 1.5, "cuota_b": 2.5},
            {"id": "C2", "peleador_a": "Ilia Topuria", "peleador_b": "Max Holloway", "cuota_a": 1.8, "cuota_b": 2.0}
        ]
    }
]

TIENDA_PRODUCTOS = [
    # Categoria: Guantes
    {"id": "P1", "nombre": "Guantes Hayabusa T3 16oz", "precio": "$160.00", "categoria": "Guantes", "img_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=500&q=80", "desc": "Soporte de muñeca patentado V-Strap. (Importación directa)."},
    {"id": "P2", "nombre": "Cleto Reyes Entrenamiento 14oz", "precio": "$220.00", "categoria": "Guantes", "img_url": "https://images.unsplash.com/photo-1512686125587-578d1cbbe190?auto=format&fit=crop&w=500&q=80", "desc": "Piel de cabra auténtica, hechos a mano. El guante de los campeones."},
    {"id": "P3", "nombre": "Winning Professional 16oz", "precio": "$380.00", "categoria": "Guantes", "img_url": "https://images.unsplash.com/photo-1596328222879-11ba106bb983?auto=format&fit=crop&w=500&q=80", "desc": "La marca #1 del mundo. Máxima protección de nudillos. (USA Import)."},
    
    # Categoria: Suplementos
    {"id": "S1", "nombre": "Creatina Nutrex Research 300g", "precio": "$30.00", "categoria": "Suplementos", "img_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=500&q=80", "desc": "Creatina monohidratada pura. Beneficio PRO: 15% de Descuento adicional."},
    {"id": "S2", "nombre": "Ronnie Coleman Signature Whey (5lbs)", "precio": "$75.00", "categoria": "Suplementos", "img_url": "https://images.unsplash.com/photo-1579722820308-d74e571900a9?auto=format&fit=crop&w=500&q=80", "desc": "Proteína premium para recuperación muscular. Sabor Vainilla/Chocolate."},
    
    # Categoria: Sacos e Implementos
    {"id": "I1", "nombre": "Saco Pesado Everlast 100lbs", "precio": "$120.00", "categoria": "Sacos e Implementos", "img_url": "https://images.unsplash.com/photo-1517838503506-3b561768809d?auto=format&fit=crop&w=500&q=80", "desc": "Trabajo de potencia extrema."},
    {"id": "I2", "nombre": "Gobernadora (Punch Shield) Title", "precio": "$85.00", "categoria": "Sacos e Implementos", "img_url": "https://images.unsplash.com/photo-1599552375246-24ee029302e3?auto=format&fit=crop&w=500&q=80", "desc": "Absorción de impacto para entrenadores profesionales."},
    
    # Categoria: Artículos de Entrenamiento
    {"id": "A1", "nombre": "Vendas Profesionales Ringside 180\"", "precio": "$15.00", "categoria": "Artículos de Entrenamiento", "img_url": "https://images.unsplash.com/photo-1595252876632-478a59483dc8?auto=format&fit=crop&w=500&q=80", "desc": "Mezcla semi-elástica para protección perfecta."},
    {"id": "A2", "nombre": "Cuerda de Saltar Pesada", "precio": "$45.00", "categoria": "Artículos de Entrenamiento", "img_url": "https://images.unsplash.com/photo-1517438476312-10d79c077509?auto=format&fit=crop&w=500&q=80", "desc": "Sistema de rodamientos de acero para velocidad."}
]
