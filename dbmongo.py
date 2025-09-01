from pymongo import MongoClient


def guardarEntrada(entrada):
    # Abrimos la puerta
    cliente = MongoClient("mongodb://localhost:27017/")

    # Escogemos un cajón (base de datos)
    db = cliente["CecarArticulo"]

    # Escogemos una caja (colección)
    coleccion = db["entradas"]

    # Guardamos un juguete (documento)
    coleccion.insert_one(entrada)
