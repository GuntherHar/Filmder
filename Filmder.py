## ::::::::::::::::::::::::::::::::: ENCABEZADO :::::::::::::::::::::::::::::::::



## :::::::::::::::::::: IMPORTACION DE MODULOS Y BIBLIOTECAS ::::::::::::::::::::

import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import json

## :::::::::::::::::::::: DEFINICION DE FUNCIONES O CLASES ::::::::::::::::::::::

class Grafo:
  def __init__(self):
      self.adyacencias = {}
      self.atributos = {}

  def leerJSON(self, ruta_archivo):
      peliculas = {}
      with open(ruta_archivo, 'r') as f:
        peliculas = json.load(f)
        return peliculas

  def crearNodo(self, nodos, peliculas):
    for nombre, atributo in peliculas.items():
      nodo = nombre
      nodos.append(nodo)
      grafo.add_node(nodo)
      self.atributos[nodo] = atributo

  def crearAristas(self, nodos):
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            nodo1, nodo2 = nodos[i], nodos[j]
            atributo1, atributo2 = self.atributos[nodo1], self.atributos[nodo2]

            # Conexión por género
            if atributo1['genero'] == atributo2['genero']:
                grafo.add_edge(nodo1, nodo2)

            # Conexión por director
            elif atributo1['director'] == atributo2['director']:
                grafo.add_edge(nodo1, nodo2)

            # Conexion por estilo visual
            elif atributo1['estilo'] == atributo2['estilo']:
                grafo.add_edge(nodo1, nodo2)

  def bfs(self, inicio):
        visitados = set()
        cola = deque([inicio])
        recorrido = []

        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                recorrido.append(nodo)
                vecinos = list(grafo.successors(nodo))
                cola.extend([vecino for vecino in vecinos if vecino not in visitados])

        return recorrido

class Filmder:
    def __init__(self):
        self.g = Grafo()
        pelicula = self.g.leerJSON('peliculas.json')
        self.watchlist = []
    
        self.g.crearNodo(nodos, pelicula)
        self.g.crearAristas(nodos)
        self.ventanaIn()

    def ventanaIn(self):
        # Creacion de la ventana inicial
        self.ventana0 = tk.Tk()
        self.ventana0.title('Filmder')
        self.ventana0.geometry('500x500+500+240')
        # Creacion del menu
        menu_principal = tk.Menu()
        menu_principal.add_command(label='Salir', command=self.ventana0.destroy)
        menu_principal.add_command(label='Watchlist', command=self.verWatchlist)

        # Busqueda de pelicula
        tk.Label(self.ventana0, text='Escriba la pelicula que le gusto', font=('Arial',12)).grid(row=0, column=0)
        self.elemento = tk.Entry(self.ventana0)
        self.elemento.grid(row=1, column=0)
        self.botonA = tk.Button(self.ventana0, text = 'Buscar', command=self.buscar)
        self.botonA.grid(row=3, column=0)

        self.ventana0.config(menu=menu_principal)
        self.ventana0.mainloop()
    
    def ventanaPr(self, pelicula):
        # Obtener datos de la película
        self.atributos = self.g.atributos[pelicula]

        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title('Filmder')
        self.ventana.geometry('500x500+500+240')

        # Crear el menu
        menu_principal = tk.Menu()
        menu_principal.add_command(label='Salir', command=self.ventana.destroy)
        menu_principal.add_command(label='Watchlist', command=self.verWatchlist)
        self.ventana.config(menu=menu_principal)

        # Datos de la pelicula
        self.titulo = tk.Label(self.ventana, text=pelicula, font=('Arial', 14, 'bold'))
        self.titulo.grid(row=0, column=0, columnspan=3, pady=10)
        self.sinopsis = tk.Label(self.ventana, text=self.atributos.get('sinopsis', 'Sinopsis no disponible'), wraplength=400, justify='left')
        self.sinopsis.grid(row=1, column=0, columnspan=3, pady=5)

        # Creacion de imagen
        self.labelImagen = tk.Label(self.ventana)
        self.labelImagen.grid(row=2, column=1, pady=10)

        # Creacion de los botones
        self.botonVisto = tk.Button(self.ventana, text="Ya la vi", command=self.siguientePeli)
        self.botonVisto.grid(row=3, column=2, pady=10)
        self.botonWatchlist = tk.Button(self.ventana, text="Añadir al Watchlist", command=self.listaPeliculas)
        self.botonWatchlist.grid(row=3, column=1, pady=10)
        self.botonNoInteresa = tk.Button(self.ventana, text="No me interesa", command=self.siguientePeli)
        self.botonNoInteresa.grid(row=3, column=0, pady=10)

        self.recomendacion(pelicula)
        self.ventana.mainloop()

    def buscar(self):
        self.peliculaBuscar = self.elemento.get()
        self.recorrido = self.g.bfs(self.peliculaBuscar)

        if len(self.recorrido) <= 1:
            self.titulo.config(text="No se encontraron recomendaciones")
            self.sinopsis.config(text="")
            return

        self.recorridoActual = self.recorrido[1:]  # omitir la película original
        self.ventana0.destroy()
        self.ventanaPr(self.recorridoActual.pop(0))

    def siguientePeli(self):
        if self.recorridoActual:
            self.recomendacion(self.recorridoActual.pop(0))
        else:
            self.titulo.config(text="¡No hay más recomendaciones!")
            self.sinopsis.config(text="")
            self.boton_visto.grid_remove()
            self.boton_no_interesa.grid_remove()
            self.boton_watchlist.grid_remove()

    def recomendacion(self, pelicula):
        # Actualizar datos 
        self.atributos = self.g.atributos[pelicula]
        self.titulo.config(text=pelicula)
        self.sinopsis.config(text=self.atributos.get('sinopsis', 'Sinopsis no disponible'))

        # Agregar la imagen
        rutaImagen = self.atributos.get('imagen', 'Ruta no encontrada')
        imagen = Image.open(rutaImagen)
        imagen = imagen.resize((200, 300))
        imagen_tk = ImageTk.PhotoImage(imagen)

        # Actualizacion de la imagen 
        self.labelImagen.config(image=imagen_tk)
        self.labelImagen.image = imagen_tk  # Referencia para que no lo borre el GC

    def listaPeliculas(self):
        peliActual = self.titulo.cget("text") 
        self.watchlist.append(peliActual)
        self.siguientePeli()

    def verWatchlist(self):
        print(self.watchlist)


## :::::::::::::::::::::::: VARIABLES U OBJETOS GLOBALES ::::::::::::::::::::::::

nodos = []
grafo = nx.DiGraph()

## :::::::::::::::::::::::::::::: BLOQUE PRINCIPAL ::::::::::::::::::::::::::::::

if __name__ == '__main__':
    f = Filmder()
    plt.gcf().canvas.manager.set_window_title('Grafo dirigido')
    nx.draw(grafo, with_labels=True)
    plt.show()

## :::::::::::::::::::::::::::::::: COMENTARIOS :::::::::::::::::::::::::::::::::
