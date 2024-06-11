from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

DATABASE_URL = "mariadb+mariadbconnector://root:1234567@127.0.0.1:3306/RecetaDB"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    ingredientes = Column(Text, nullable=False)
    pasos = Column(Text, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def agregar_receta(nombre, ingredientes, pasos):
    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    try:
        session.add(nueva_receta)
        session.commit()
        print("Receta agregada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al agregar la receta: {e}")

def actualizar_receta(id_receta, nombre, ingredientes, pasos):
    try:
        receta = session.query(Receta).filter(Receta.id == id_receta).one()
        receta.nombre = nombre
        receta.ingredientes = ingredientes
        receta.pasos = pasos
        session.commit()
        print("Receta actualizada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al actualizar la receta: {e}")

def eliminar_receta(id_receta):
    try:
        receta = session.query(Receta).filter(Receta.id == id_receta).one()
        session.delete(receta)
        session.commit()
        print("Receta eliminada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al eliminar la receta: {e}")

def ver_listado_recetas():
    try:
        recetas = session.query(Receta).all()
        if recetas:
            for receta in recetas:
                print(f"ID: {receta.id}, Nombre: {receta.nombre}")
        else:
            print("No hay recetas en la base de datos.")
    except Exception as e:
        print(f"Error al obtener el listado de recetas: {e}")

def buscar_receta_por_ingredientes(ingredientes):
    try:
        recetas = session.query(Receta).filter(Receta.ingredientes.like(f"%{ingredientes}%")).all()
        if recetas:
            for receta in recetas:
                print(f"Nombre: {receta.nombre}")
                print(f"Ingredientes: {receta.ingredientes}")
                print(f"Pasos: {receta.pasos}")
                print()
        else:
            print("No se encontraron recetas con esos ingredientes.")
    except Exception as e:
        print(f"Error al buscar recetas por ingredientes: {e}")

def buscar_receta_por_pasos(pasos):
    try:
        recetas = session.query(Receta).filter(Receta.pasos.like(f"%{pasos}%")).all()
        if recetas:
            for receta in recetas:
                print(f"Nombre: {receta.nombre}")
                print(f"Ingredientes: {receta.ingredientes}")
                print(f"Pasos: {receta.pasos}")
                print()
        else:
            print("No se encontraron recetas con esos pasos.")
    except Exception as e:
        print(f"Error al buscar recetas por pasos: {e}")

def main():
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar recetas por ingredientes")
        print("f) Buscar recetas por pasos")
        print("g) Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            nombre = input("Nombre de la receta: ")
            ingredientes = input("Ingredientes (separados por comas): ")
            pasos = input("Pasos de la receta: ")
            agregar_receta(nombre, ingredientes, pasos)
        elif opcion == 'b':
            id_receta = int(input("ID de la receta a actualizar: "))
            nombre = input("Nuevo nombre de la receta: ")
            ingredientes = input("Nuevos ingredientes (separados por comas): ")
            pasos = input("Nuevos pasos de la receta: ")
            actualizar_receta(id_receta, nombre, ingredientes, pasos)
        elif opcion == 'c':
            id_receta = int(input("ID de la receta a eliminar: "))
            eliminar_receta(id_receta)
        elif opcion == 'd':
            ver_listado_recetas()
        elif opcion == 'e':
            ingredientes = input("Ingrese los ingredientes a buscar: ")
            buscar_receta_por_ingredientes(ingredientes)
        elif opcion == 'f':
            pasos = input("Ingrese los pasos a buscar: ")
            buscar_receta_por_pasos(pasos)
        elif opcion == 'g':
            print("Adios owo/")
            session.close()
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
