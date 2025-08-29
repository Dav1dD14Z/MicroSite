from fastapi import FastAPI, HTTPException, status
from models.products import Producto
import sqlite3

app = FastAPI()

@app.get("/")
def start():
    return {"message": "Hi class"}

@app.get("/database/")
def create_db():
    #funcion para crear la base de datos en sqlite con campos id, name, price
    conn = sqlite3.connect('microsite.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    return {"message": "Database created successfully"}, status.HTTP_201_CREATED

@app.post("/productos/")
def crear_producto(producto: Producto):
    conn = sqlite3.connect('microsite.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (name, price) VALUES (?, ?)
    ''', (producto.name, producto.price))
    conn.commit()
    conn.close()
    return {
        "message": "Producto creado correctamente",
        "data": producto.dict()
    }

@app.get("/productos/")
def listar_productos():
    conn = sqlite3.connect('microsite.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return {
        "message": "Lista de productos",
        "data": [{"id": row[0], "nombre": row[1], "precio": row[2]} for row in productos]
    }