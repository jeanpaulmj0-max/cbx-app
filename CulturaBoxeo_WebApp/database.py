import sqlite3
import hashlib
import os
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "culturaboxeo.db")

# ==========================================
# CONEXIÓN A SUPABASE (NUBE) O SQLITE (LOCAL)
# ==========================================
supabase = None
try:
    if "supabase" in st.secrets:
        from supabase import create_client
        url = st.secrets["supabase"]["URL"]
        key = st.secrets["supabase"]["KEY"]
        supabase = create_client(url, key)
except Exception as e:
    pass

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    if supabase:
        # En Supabase la tabla ya fue creada por el usuario vía SQL. No hacemos nada.
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 1. Tabla original de usuarios (se mantiene para no romper el login)
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT,
                  apellido TEXT,
                  email TEXT UNIQUE,
                  password_hash TEXT,
                  gym_origen TEXT,
                  cbx_coins INTEGER DEFAULT 1000,
                  is_premium BOOLEAN DEFAULT 0,
                  rol TEXT DEFAULT 'free',
                  xp INTEGER DEFAULT 0,
                  photo_blob BLOB)''')
                  
    # 2. Nuevas tablas CORE (Rounds Architecture)
    c.execute('''CREATE TABLE IF NOT EXISTS branches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS classes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  branch_id INTEGER,
                  name TEXT,
                  FOREIGN KEY(branch_id) REFERENCES branches(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS seasons
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  year INTEGER,
                  start_date TEXT,
                  end_date TEXT)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS training_sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  class_id INTEGER,
                  date TEXT,
                  FOREIGN KEY(user_id) REFERENCES usuarios(id),
                  FOREIGN KEY(class_id) REFERENCES classes(id))''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS wellness_checkins
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id INTEGER,
                  mood TEXT,
                  energy INTEGER,
                  fatigue INTEGER,
                  recovery INTEGER,
                  motivation INTEGER,
                  learning_gap TEXT,
                  FOREIGN KEY(session_id) REFERENCES training_sessions(id))''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  coach_id INTEGER,
                  class_id INTEGER,
                  message TEXT,
                  date TEXT,
                  FOREIGN KEY(coach_id) REFERENCES usuarios(id),
                  FOREIGN KEY(class_id) REFERENCES classes(id))''')

    # Seed inicial si las sedes no existen
    c.execute("SELECT count(*) FROM branches")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO branches (name) VALUES ('Rounds - Matriz')")
        c.execute("INSERT INTO branches (name) VALUES ('Best Training')")
        c.execute("INSERT INTO branches (name) VALUES ('CrossFit Company')")
        
    conn.commit()
    
    # Manejar ALTER TABLE para usuarios viejos que no tienen photo_blob
    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN photo_blob BLOB")
        conn.commit()
    except:
        pass # La columna ya existe
        
    conn.close()

def register_user(nombre, apellido, email, password, gym_origen, codigo_staff=""):
    if not all([nombre, apellido, email, password]):
        return False, "Todos los campos son obligatorios."
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
        
    rol = "member" if "Socio" in gym_origen else "free"
    
    # FILTRO SECRETO PARA ENTRENADORES (OPCIÓN 1)
    if codigo_staff == "ROUNDS-COACH-2026":
        rol = "coach"
    elif codigo_staff.strip() != "" and codigo_staff != "ROUNDS-COACH-2026":
        return False, "Código de Staff inválido. Si eres alumno, deja el campo vacío."
        
    is_premium = 1 if rol in ["member", "pro", "coach"] else 0
    hashed_pw = hash_password(password)
    
    if supabase:
        try:
            # Verificar si existe
            res = supabase.table("usuarios").select("email").eq("email", email.strip().lower()).execute()
            if len(res.data) > 0:
                return False, "El correo electrónico ya está registrado."
                
            nuevo = {
                "nombre": nombre.strip(),
                "apellido": apellido.strip(),
                "email": email.strip().lower(),
                "password_hash": hashed_pw,
                "gym_origen": gym_origen,
                "cbx_coins": 1000,
                "is_premium": is_premium,
                "rol": rol,
                "xp": 0
            }
            supabase.table("usuarios").insert(nuevo).execute()
            return True, "Registro exitoso"
        except Exception as e:
            return False, f"Error en la base de datos (Nube): {str(e)}"
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO usuarios (nombre, apellido, email, password_hash, gym_origen, cbx_coins, is_premium, rol, xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (nombre.strip(), apellido.strip(), email.strip().lower(), hashed_pw, gym_origen, 1000, is_premium, rol, 0))
            conn.commit()
            return True, "Registro exitoso (Local)"
        except sqlite3.IntegrityError:
            return False, "El correo electrónico ya está registrado."
        finally:
            conn.close()

def authenticate_user(email, password):
    hashed_pw = hash_password(password)
    email_clean = email.strip().lower()
    
    if supabase:
        try:
            res = supabase.table("usuarios").select("*").eq("email", email_clean).eq("password_hash", hashed_pw).execute()
            if len(res.data) > 0:
                return True, res.data[0]
            return False, "Correo o contraseña incorrectos."
        except Exception as e:
            return False, f"Error conectando a la nube."
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, nombre, apellido, email, gym_origen, cbx_coins, rol, xp FROM usuarios WHERE email=? AND password_hash=?",
                  (email_clean, hashed_pw))
        user = c.fetchone()
        conn.close()
        if user:
            return True, {
                "id": user[0], "nombre": user[1], "apellido": user[2], "email": user[3],
                "gym_origen": user[4], "cbx_coins": user[5], "rol": user[6], "xp": user[7]
            }
        return False, "Correo o contraseña incorrectos."

def update_coins(user_id, amount):
    if supabase:
        res = supabase.table("usuarios").select("cbx_coins").eq("id", user_id).execute()
        if res.data:
            new_coins = res.data[0]["cbx_coins"] + amount
            supabase.table("usuarios").update({"cbx_coins": new_coins}).eq("id", user_id).execute()
            return new_coins
        return 0
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE usuarios SET cbx_coins = cbx_coins + ? WHERE id = ?", (amount, user_id))
        conn.commit()
        c.execute("SELECT cbx_coins FROM usuarios WHERE id = ?", (user_id,))
        nuevo_saldo = c.fetchone()[0]
        conn.close()
        return nuevo_saldo

def add_xp(user_id, amount):
    if supabase:
        res = supabase.table("usuarios").select("xp").eq("id", user_id).execute()
        if res.data:
            new_xp = res.data[0]["xp"] + amount
            supabase.table("usuarios").update({"xp": new_xp}).eq("id", user_id).execute()
            return new_xp
        return 0
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE usuarios SET xp = xp + ? WHERE id = ?", (amount, user_id))
        conn.commit()
        c.execute("SELECT xp FROM usuarios WHERE id = ?", (user_id,))
        nuevo_xp = c.fetchone()[0]
        conn.close()
        return nuevo_xp
