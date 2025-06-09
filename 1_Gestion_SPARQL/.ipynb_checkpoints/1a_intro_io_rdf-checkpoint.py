# %% [markdown]
# # Grafos rdflib: entrada/salida RDF
#  
# 1. `g1 = rdflib.Graph()` crea un grafo en memoria, vacío de tripletas, al que se accede a través de la variable (p.ej, en este caso, `g1`). Un grafo rdflib es un contenedor de un conjunto de 3-tuplas: [(s1,p1,o1), (s2,p2,o2), ..., (sN,pN,oN)].
# 2. `g1.parse(...)` lee texto en cualquiera de los formatos RDF en que se pueden declarar tripletas y las incorpora al grafo `g1` en memoria. Desde un mismo grafo, como `g1`, se pueden leer sucesivamente nuevos textos RDF y se irán incorporando tan sólo nuevas tripletas (las que no estuvieran ya en el grafo `g1`)
# 3. `g1.serialize(...)` exporta tripletas del grafo `g1` a un texto RDF en cualquiera de los formatos disponibles.

Los dos métodos anteriores leen o escriben directamente a/desde una cadena de texto o a/desde un fichero (o url).

# %% [markdown]
# ## 1. Entrada/salida como cadena de texto

# %% [markdown]
# ### 1.1 Instanciación de un grafo

# %%
import rdflib

g1 = rdflib.Graph()

# %% [markdown]
# ### 1.2 Tripletas cargadas desde un texto RDF
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

print(f"Ejecución. Hay un total de {len(g1)} tripletas en el grafo.")

# %% [markdown]
# ### 1.3 Tripletas secuenciadas a un texto RDF
# **Secuenciación e impresión** de las tripletas del grafo. Se puede escoger el formato RDF de salida.

# %%
txt1_nt = g1.serialize(format='nt')

print("Grafo en formato N-Triples:")
print(txt1_nt)

# %% [markdown]
# ## 2. Entrada incremental de nuevas tripletas
#
# 1. Se enuncia otro texto RDF `txt2_turtle` con nuevas tripletas, salvo 2 de ellas que ya estaban declaradas en el texto turtle `txt1_turtle` de inicio de este cuaderno.
# 2. Se incorporan estas tripletas al grafo `g1`. Se puede apreciar que las 2 tripletas repetidas no se han duplicado internamente porque un grafo rdflib es un **conjunto** de 3-tuplas (todas ellas distintas entre sí).

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

# %% [markdown]
# La declaración de Comunidad como Clase y de Provincia como Clase ya aparecían identicamente expresadas en el texto RDF inicial `txt1_turtle`. Se descartará su inclusión duplicada en `g1`.

# %%
g1.parse(data=txt2_turtle, format="turtle")

print(f"Ejecución. Ahora el grafo tiene un total de {len(g1)} tripletas.")

# %% [markdown]
# El grafo contiene las tripletas que ya tenía **más las nuevas** que se han incorporado. Hay dos tripletas en el anterior documento que ya existían en el primero; en concreto, las declaraciones de Comunidad y de Provincia como clases, que ya contenía el grafo y que no duplica.

# %%
# Se secuencia el grafo a formato N-Triples
txt_1_y_2 = g1.serialize(format='turtle')

print("Grafo, ampliado, en formato Turtle:")
print(txt_1_y_2)


# %% [markdown]
# ## 3. Carga/descarga en ficheros
#
# 1. Se almacena el grafo `g1` anterior en un fichero RDF `prueba_almacenamiento.jsonld`: _g.serialize(**destination=**'prueba_almacenamiento.jsonld', format='json-ld')_. Como formato RDF de salida, entre otros posibles, se ha escogido json-ld.
# 2. Se crea un nuevo grafo vacío `g2`y se carga con el contenido del fichero anterior: _g2.parse(**location=**'prueba_almacenamiento.jsonld', format='json-ld')_ De esta forma, `g2` contiene, de momento, las mismas ternas que `g1`.

# %%
fich_salida = 'prueba_almacenamiento'
g1.serialize(destination=fich_salida, format='json-ld')
print(f"Ejecución. Fichero {fich_salida} creado con las tripletas del grafo `g1` expresadas en formato json-ld.")

# %%
g2 = rdflib.Graph()
g2.parse(location=fich_salida, format='json-ld')
print(f"Ejecución. Nuevo grafo `g2`, cargado con las tripletas declaradas en el fichero {fich_salida} en formato json-ld.")

# %%
print("En este punto, los grafos `g1` y `g2` deberían contener las mismas tripletas:")
print(g2.serialize(format='nt'))

