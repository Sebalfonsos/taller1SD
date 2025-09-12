from pymongo import MongoClient
from bson.objectid import ObjectId

# Reutilizamos la conexión siempre que se importe este módulo
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["CecarArticulo"]
coleccion = db["entradas"]

def guardarEntrada(entrada):
    """Guarda un documento en la colección"""
    return coleccion.insert_one(entrada)

def get_all_paginated(page=1, per_page=20):
    """Obtiene documentos paginados"""
    skip = (page - 1) * per_page
    cursor = coleccion.find().skip(skip).limit(per_page)
    return list(cursor)

def get_count():
    """Devuelve la cantidad total de documentos"""
    return coleccion.count_documents({})

def get_by_id(id_str):
    """Busca un documento por su _id"""
    return coleccion.find_one({"_id": ObjectId(id_str)})
