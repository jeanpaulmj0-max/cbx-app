import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import ssl
import re

def fetch_live_news():
    # Evitar errores de certificado SSL en algunas máquinas
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    noticias = []
    # Fuentes RSS en español (Boxeo / MMA)
    fuentes = [
        {"url": "https://www.soloboxeo.com/feed/", "nombre": "SoloBoxeo"},
        {"url": "https://superluchas.com/feed/", "nombre": "SuperLuchas"}
    ]
    
    try:
        for fuente in fuentes:
            req = urllib.request.Request(fuente["url"], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # Buscar los primeros artículos
                for item in root.findall('.//item'):
                    titulo = item.find('title').text if item.find('title') is not None else "Sin Título"
                    link = item.find('link').text if item.find('link') is not None else "#"
                    
                    # Buscar imagen (usualmente en contenido)
                    imagen_url = "https://images.unsplash.com/photo-1599552375246-24ee029302e3?auto=format&fit=crop&w=1000&q=80" # Default
                    
                    desc = item.find('description')
                    content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
                    
                    html_text = ""
                    if content is not None and content.text:
                        html_text = content.text
                    elif desc is not None and desc.text:
                        html_text = desc.text
                        
                    if html_text:
                        img_match = re.search(r'src="([^"]+)"', html_text)
                        if img_match:
                            imagen_url = img_match.group(1)

                    noticias.append({
                        "id": str(abs(hash(titulo))),
                        "titulo": titulo,
                        "subtitulo": "Reporte de última hora desde " + fuente["nombre"],
                        "fecha": datetime.now().strftime("%d de %B, %Y"),
                        "fuente": fuente["nombre"].upper(),
                        "categoria": "ACTUALIDAD",
                        "imagen_url": imagen_url,
                        "contenido_html": f"<p>{html_text[:200]}...</p><p><a href='{link}' target='_blank'>Leer fuente original</a></p>"
                    })
                    
                    if len(noticias) >= 6:
                        break
            if len(noticias) >= 6:
                break
                
    except Exception as e:
        print(f"Error extrayendo noticias: {e}")
        
    return noticias[:6]
