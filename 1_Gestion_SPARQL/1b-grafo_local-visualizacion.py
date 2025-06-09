# %% [markdown]
# # Grafos: visualización
#
# ## Resumen del cuaderno 
# 1. **El lenguaje DOT** es un lenguaje genérico para declarar grafos (no sólo RDF) como se puede apreciar en su [Guía de usuario](https://www.graphviz.org/pdf/dotguide.pdf)
# 2. **La aplicación Graphviz** es una aplicación de línea de comando que calcula la posición adecuada de los nodos de un grafo dot para visualizarlo o para exportarla a un fichero (en diversos formatos gráficos).
# 3. **rdf2dot** es un funcion Python que genera una descripción en lenguaje DOT de un grafo rdflib en memoria. El grafo dot generado se puede visualizar o exportar a un fichero, escogiendo el formato gráfico.
#
# La visualización de grafos RDF permite seguir mejor la presentación ejemplos de procesamiento de estos grafos (para grafos RDF pequeños). Graphviz tan sólo facilita una visualización estática pero con un adecuado posicionamiento automático de nodos. Para grafos muy grandes convendrá utilizar aplicaciones interactivas que permiten navegar por el grafo: ocultar selectivamente nodos y enlaces, así como irlos mostrando puntualmente bajo demanda.


# %% [markdown]
# ## 1. Un primer grafo para visualizar

# %%
import rdflib
g = rdflib.Graph()

# %%
txt1_turtle = '''
@prefix ej: <http://uned.es/ejs/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ej:Comunidad rdf:type rdfs:Class .
ej:Provincia rdf:type rdfs:Class .

# Provincias de la Comunidad Valenciana
ej:Comunidad_Valenciana ej:tiene_provincia ej:Alicante_prov , ej:Valencia_prov , ej:Castellon_prov ;
                        rdf:type ej:Comunidad .

# Algunos municipios en las provincias de la Comunidad Valenciana
ej:Alicante_prov ej:tiene_municipio ej:Alicante_munic , ej:Elche ;
                 rdf:type ej:Provincia .
ej:Valencia_prov ej:tiene_municipio ej:Valencia_munic , ej:Gandia ;
                 rdf:type ej:Provincia .
ej:Castellon_prov ej:tiene_municipio ej:Castellon_de_la_Plana , ej:Villareal ;
                  rdf:type ej:Provincia .
'''

# %%
g.parse(data=txt1_turtle, format="turtle")

# %% [markdown]
# ## 2. Visualización con rdf2dot + graphviz
# El paquete graphviz de Python requiere que se encuentre instalada la aplicación [graphviz](https://www.graphviz.org/download/) en el sistema.

# %%
from rdflib.tools.rdf2dot import rdf2dot
from io import StringIO
import graphviz

# %% [markdown]
# La función rdf2dot escribe las tripletas del grafo en el string en lenguaje dot (con ciertas opciones por defecto sobre el estilo de presentación)

# %%
sio1 = StringIO()
rdf2dot(g, sio1)
dot_source1 = sio1.getvalue()

# %% [markdown]
# El grafo dot contiene declaraciones estructurales iniciales sobre nodos y enlaces, seguidas de declaraciones opcionales sobre estilo de presentación

# %%
print(dot_source1)


# %% [markdown]
# Se construye una presentación a partir de la declaración del grafo en formato dot y se muestra directamente en el cuaderno Jupyter.

# %%
gv1 = graphviz.Source(dot_source1)
gv1  

# %% [markdown]
# ## 2. Grafo ampliado y revisualizado
# Se añaden nuevas tripletas al grafo inicial y se visualiza este grafo ampliado.

# %%
txt2_turtle = '''
@prefix ej: <http://uned.es/ejs/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ej:Comunidad rdf:type rdfs:Class .
ej:Provincia rdf:type rdfs:Class .

# Se declara Extremadura de tipo Comunidad y se enlaza con sus provincias
ej:Extremadura ej:tiene_provincia ej:Caceres_prov , ej:Badajoz_prov ;
               rdf:type ej:Comunidad .

# Algunos municipios en las provincias de Extremadura
ej:Caceres_prov ej:tiene_municipio ej:Caceres_munic , ej:Plasencia ;
                rdf:type ej:Provincia .      
ej:Badajoz_prov ej:tiene_municipio ej:Badajoz_munic , ej:Merida ;
                rdf:type ej:Provincia .
'''

# %%
g.parse(data=txt2_turtle, format="turtle")

# %%
sio2 = StringIO()
rdf2dot(g, sio2)
dot_source2 = sio2.getvalue()


# %%
gv2 = graphviz.Source(dot_source2)
gv2  

# %% [markdown]
# ## 3. Almacenamiento en ficheros y recuperación

# %% [markdown]
# ### 3.1 Ficheros gráficos
# La presentación producida se puede almacenar en un fichero escogiendo el formato gráfico (png, svg, etc)

# %%
camino_fich = gv2.render(filename='fichs/1b-visualizacion_grafo_rdf', format='svg', cleanup=True)
print(f"SVG guardado en: {camino_fich}")

# %% [markdown]
# Como ocurre con cualquier imagen, este fichero svg se puede visualizar en una celda Markdown como ésta mediante un enlace (descomentado) como `![Gráfico](fichs/1b-visualizacion_grafo_rdf.svg)`.
# Si lo que se desea es recuperarlo en una celda de código y visualizarlo, se puede utilizar la siguiente funcion:

# %%
from IPython.display import SVG, display

# Si el fichero está en el mismo directorio del notebook:
display(SVG(filename='fichs/1b-visualizacion_grafo_rdf.svg'))

# %% [markdown]
# ### 3.2 Ficheros dot, para su gestión externa
# Los ficheros dot producidos por rdf2dot se pueden almacenar externamente como ficheros de texto (usualmente, con extension .dot). 

# %%
with open("fichs/1b-grafo_rdf.dot", "w", encoding="utf-8") as f:
    f.write(dot_source2)
print("Fichero .dot guardado")

# %% [markdown]
# Esto permite su recuperación desde cualquier cuaderno Jupyter para utilizar su contenido de nuevo en `graphviz.Source(contenido)`.
# Alternativamente, estos ficheros .dot se pueden convertir _externamente en un terminal_ a cualquier formato gráfico sin uso de Jupyter ni programación Python. Basta usar los comandos de la aplicación graphviz instalada en el sistema:
#
# `dot -Tsvg grafo.dot -o grafo.svg`
#
# `dot -Tpng grafo.dot -o grafo.png`
#
#

