# mock_data.py
# Capa de datos para Cultura de Boxeo V1.0

ENTRENAMIENTOS = {
    "🔥 DROP 1: FUNDAMENTOS DEL STRIKING (Próximamente)": [
        {
            "id": "T01", "titulo": "Postura, Guardia y Desplazamiento", "nivel_orden": "Episodio 1",
            "descripcion": "La base de todo peleador. Aprende a pararte como un profesional y moverte sin cruzar las piernas.",
            "duracion": "10 min", "objetivo": "Técnica Base", "equipamiento": "Ninguno",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Lunes, 7 de Septiembre",
            "instrucciones": "Mantén tu centro de gravedad bajo.",
            "acceso": "free"
        },
        {
            "id": "T02", "titulo": "Mecánica del Jab y Recto", "nivel_orden": "Episodio 2",
            "descripcion": "El 1-2. Cómo generar poder desde la cadera y no solo con los brazos.",
            "duracion": "15 min", "objetivo": "Precisión y Poder", "equipamiento": "Ninguno",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Miércoles, 9 de Septiembre",
            "instrucciones": "Gira el pie trasero al lanzar el recto.",
            "acceso": "free"
        }
    ],
    "🥊 RUTINAS CBX STUDIO (Exclusivo Socios)": [
        {
            "id": "T03", "titulo": "HIIT Boxeo: Sombra de Alta Intensidad", "nivel_orden": "Rutina 1",
            "descripcion": "Quema de calorías máxima simulando 3 rounds de campeonato.",
            "duracion": "20 min", "objetivo": "Cardio y Resistencia", "equipamiento": "Ninguno",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Viernes, 11 de Septiembre",
            "instrucciones": "Sigue el ritmo del coach sin bajar la guardia.",
            "acceso": "member"
        },
        {
            "id": "T04", "titulo": "Destrucción de Costal", "nivel_orden": "Rutina 2",
            "descripcion": "Trabajo de potencia en el saco pesado enfocándose en ganchos al cuerpo.",
            "duracion": "30 min", "objetivo": "Potencia", "equipamiento": "Saco, Vendas, Guantes",
            "video_url": None, "estado": "proximamente", "fecha_drop": "Por anunciar",
            "instrucciones": "Asegúrate de vendar correctamente tus manos.",
            "acceso": "member"
        }
    ],
    "🛠️ CLINIC DE SPARRING (En Construcción)": [
        {
            "id": "T05", "titulo": "Gestión de Distancia y Tiempos", "nivel_orden": "Próximamente",
            "descripcion": "Módulo avanzado en desarrollo. Aprende a leer los tiempos de tu oponente.",
            "duracion": "-- min", "objetivo": "Sparring", "equipamiento": "Casco, Bucal, Guantes 16oz",
            "video_url": None, "estado": "construccion", "fecha_drop": "Octubre 2026",
            "instrucciones": "Módulo en grabación.",
            "acceso": "pro"
        }
    ]
}

NOTICIAS = [
    {
        "id": "N1", "titulo": "Flip Jercovich sorprende a Moses Itauma y es nuevo campeón FIB", 
        "subtitulo": "El peso pesado británico sufre su primera derrota profesional en un nocaut sorpresivo.",
        "categoria": "Boxeo", "fecha": "2026-09-01", "fuente": "NotiFight", "idioma": "ES",
        "contenido_html": "<p>En una de las mayores sorpresas del fin de semana, <b>Flip Jercovich</b> logró noquear al súper prospecto británico <b>Moses Itauma</b> en el sexto asalto para coronarse como el nuevo campeón interino de los pesados de la FIB.</p><p>Itauma, quien era visto como el futuro de la división, dominó los primeros tres asaltos con su velocidad característica, pero Jercovich logró acortar la distancia e impuso su poder físico.</p><p>El nocaut vino tras un volado de derecha perfecto que apagó las luces de Itauma. El mundo del boxeo está en shock ante este resultado.</p>",
        "imagen_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", 
        "url_original": "#"
    },
    {
        "id": "N2", "titulo": "La revolución del Boxeo Femenino en 2026", 
        "subtitulo": "Las carteleras femeninas rompen récords de audiencia.",
        "categoria": "Negocios", "fecha": "2026-08-30", "fuente": "Izquierdazo", "idioma": "ES",
        "contenido_html": "<p>Con la reciente victoria de Katie Taylor y Claressa Shields reafirmando su dominio, el boxeo femenino ha logrado un pico histórico de televidentes a nivel mundial.</p><p>Los patrocinadores principales han incrementado sus presupuestos en un 40% para peleas de campeonato mundial femenino.</p>",
        "imagen_url": "https://images.unsplash.com/photo-1595252876632-478a59483dc8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", 
        "url_original": "#"
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
    {"id": "P1", "nombre": "Guantes Rival RS11V Evolution (USA Import)", "precio": "$159.00", "categoria": "Guantes Premium", "img": "🥊", "desc": "Importados directamente de USA. Sistema V-Strap patentado de Rival. Ideales para sparring profesional."},
    {"id": "P2", "nombre": "Casco Hayabusa T3 Headgear", "precio": "$135.00", "categoria": "Protección", "img": "🪖", "desc": "Diseño de perfil bajo con máxima visibilidad. Importación bajo pedido (10-15 días)."},
    {"id": "P3", "nombre": "Vendas Title Boxing Mexican Style 180\"", "precio": "$15.00", "categoria": "Accesorios", "img": "🩹", "desc": "Mezcla semi-elástica para el ajuste perfecto. Estilo mexicano profesional."},
    {"id": "P4", "nombre": "Botas Everlast Elite High Top", "precio": "$110.00", "categoria": "Calzado", "img": "👟", "desc": "Colaboración exclusiva con Michelin para máxima tracción en el ring. Suela ultra ligera."}
]
