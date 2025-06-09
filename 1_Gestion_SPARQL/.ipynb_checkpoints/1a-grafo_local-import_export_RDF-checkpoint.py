# %% [markdown]
# [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jlfvindel/grafos_RDF/blob/main/1_Gestion_SPARQL/1a-grafo_local-import_export_RDF.ipynb)

# %% [markdown]
# # Grafos: importación/exportación RDF
#
# ## Resumen del cuaderno
# 1. **Creación de un grafo**: `g1 = rdflib.Graph()` crea un grafo en memoria al que se accede a través de la variable (p.ej, en este caso, `g1`). 
# 2. **Carga de tripletas RDF a un grafo**: `g1.parse(data=...,format=...)` lee cadenas de texto en cualquier formato RDF y `g1.parse(location=...,format=...)` lee directamente tripletas RDF almacenadas en un fichero o url.
# 3. **Exportación de tripletas RDF desde un grafo**: `g1.serialize(format=...)` exporta tripletas del grafo `g1` a una cadena de texto RDF y `g1.serialize(destination=...,format=...)` escribe directamente las tripletas de `g1` en un fichero.

# %% [markdown]
# ## 1. Creación de un grafo rdflib
# Se crea un grafo vacío de tripletas. Esta instancia servirá como contenedor de un conjunto de 3-tuplas RDF: {(s1,p1,o1), (s2,p2,o2), ..., (sN,pN,oN)}. 

# %%
import rdflib

g1 = rdflib.Graph()

# %% [markdown]
# ## 2. Carga/descarga de tripletas usando cadenas de texto RDF

# %% [markdown]
# ### 2.1 Tripletas cargadas desde un texto RDF
# **Formatos**. En este ejemplo, las tripletas se declaran en un texto en formato Turtle. Se podía haber partido desde un texto en cualquiera de los [formatos RDF](https://rdflib.readthedocs.io/en/stable/plugin_parsers.html).

# %%
# Provincias de Extremadura, con algunos de sus municipios

txt1_turtle = '''
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

# %% [markdown]
# **Incorporación al grafo** de las tripletas declaradas en el texto `txt1_turtle`.  El método [parse](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) permite precisar los datos que se van a analizar y el formato en que se encuentran: _g.parse(**data=**..., format=...)_.

# %%
g1.parse(data=txt1_turtle, format="turtle")

print(f"Ejecución. Hay un total de {len(g1)} tripletas en el grafo g1.")

# %% [markdown]
# ### 2.2 Tripletas exportadas a un texto RDF
# **Secuenciación e impresión** de las tripletas del grafo. Se puede escoger el formato RDF de salida.

# %%
txt1_nt = g1.serialize(format='nt')

print("Grafo en formato N-Triples:")
print(txt1_nt)


# %% [markdown]
# ## 3. Carga/descarga de tripletas usando ficheros
# En este caso las cadenas de texto en algún formato RDF se encuentran externamente en algún fichero.
#
# ### 3.1 Descarga en ficheros
# Se almacena el contenido dle grafo `g1` en un fichero externo, escogiendo el formato RDF de secuenciación. Esta acción se puede ejecutar directamente desde `g1.serialize(destination=..., format=...)`. Tan sólo en caso de que la ruta contenga subdirectorios intermedios aún no existentes se puede requerir el uso previo de `os.makedirs`.

# %%
import os

ruta1 = "fichs/1a-comunid_prov_munic.jsonld"

# Crea todos los directorios intermedios si no existen:
os.makedirs(os.path.dirname(ruta1), exist_ok=True)

# Graba el fichero en la ruta especificada directamente desde el método serialize
g1.serialize(destination=ruta1, format='json-ld')
print(f"Ejecución. Fichero en formato jsonld creado con las tripletas del grafo `g1`.")

# %% [markdown]
# Procedimento alternativo: se usa el procedimiento general de apertura y escritura de ficheros. En este caso se ha escogido secuenciar la exportación del grafo en otro formato distinto (turtle).

# %%
ruta2 = "fichs/1a-comunid_prov_munic.ttl"

# Crea todos los directorios intermedios si no existen:
os.makedirs(os.path.dirname(ruta2), exist_ok=True)

# Usa la escritura general de ficheros para grabar el contenido de g1 secuenciado como turtle
with open(ruta2, "w", encoding="utf-8") as f:
    f.write(g1.serialize(format="turtle"))

# %% [markdown]
# ### 3.2 Carga desde un fichero
# Se crea un nuevo grafo vacío `g2`y se carga con uno de los ficheros a los que se exportó el contenido de `g1`. De esta forma, `g2` contiene, de momento, las mismas ternas que `g1`.

# %%
g2 = rdflib.Graph()
g2.parse(location='fichs/1a-comunid_prov_munic.jsonld', format='json-ld')
print(f"Ejecución. Nuevo grafo `g2`, cargado con las tripletas declaradas en el fichero jsonld en que salvó el grafo `g1`.")

# %%
print("En este punto, los grafos `g1` y `g2` deberían contener las mismas tripletas:")
print(g2.serialize(format='nt'))


# %% [markdown]
# ## 4. Cargas reiteradas sobre un mismo grafo
#
# Sobre un grafo con tripletas se puede repetir una carga adicional mediante `parse()`. En este punto hay que recordar que un grafo contiene *un conjunto* Python de tripletas, que no admite duplicidades. Por tanto, cargas reiteradas sobre un mismo grafo **tan sólo incorporan tripletas nuevas que no estuvieran ya en el grafo**.
#
# A continuación se declaran nuevas tripletas en un texto turtle que se van a incorporar al grafo `g2`. De este nuevo texto `txt2_turtle`,  la declaración de Comunidad como Clase y de Provincia como Clase ya aparecían identicamente expresadas en el texto RDF inicial `txt1_turtle`. No se duplicarán en `g2`.

# %%
# Provincias de la Comunidad Valenciana, con algunos de sus municipios

txt2_turtle = '''
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
g2.parse(data=txt2_turtle, format="turtle")

print(f"El grafo g1 mantiene un total de {len(g1)} tripletas.")
print(f"El grafo g2, tras su ampliación, tiene un total de {len(g2)} tripletas.")


# %% [markdown]
# El grafo contiene las tripletas que ya tenía **más las nuevas** que se han incorporado.

# %%
# Se secuencia el grafo a formato Turtle y se imprime
print("Grafo, ampliado, en formato Turtle:")
print(g2.serialize(format='turtle'))




