# %% [markdown]
# # Consultas SPARQL CONSTRUCT a un grafo local


# %% [markdown]
# ## Resumen del cuaderno
# 1. `grafo.query(consulta)`: el método _query_ se utiliza indistintamente para consultas SELECT o CONSTRUCT (y más adelante, para consultas UPDATE); tan sólo difiere internamente la redacción  SPARQL de la consulta.
# 2. **Una consulta CONSTRUCT devuelve un grafo como resultado**. Conviene recordar que una consulta SELECT devolvía una tabla de resultados: varias filas sobre las mismas N-columnas.

# %% [markdown]
# ## 1 Grafo consultado

# %%
import rdflib

g_orig = rdflib.Graph()

# %%
txt_turtle = '''
@prefix ej: <http://uned.es/ejs/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ej:Comunidad rdf:type rdfs:Class .
ej:Provincia rdf:type rdfs:Class .

# Se declara Extremadura de tipo Comunidad y se enlaza con sus provincias
ej:Extremadura ej:tiene_provincia ej:Cáceres_prov , ej:Badajoz_prov ;
               rdf:type ej:Comunidad .

# Algunos municipios en las provincias de Extremadura
ej:Cáceres_prov ej:tiene_municipio ej:Cáceres_munic , ej:Plasencia ;
                rdf:type ej:Provincia .      
ej:Badajoz_prov ej:tiene_municipio ej:Badajoz_munic , ej:Mérida ;
                rdf:type ej:Provincia .
'''

g_orig.parse(data=txt_turtle, format="turtle")

# %%
from rdflib.tools.rdf2dot import rdf2dot
from io import StringIO
import graphviz

# %% [markdown]
# Visualización del grafo consultado.

# %%
sio_orig = StringIO()
rdf2dot(g_orig, sio_orig)
dot_source_orig = sio_orig.getvalue()

gv_orig = graphviz.Source(dot_source_orig)
gv_orig 


# %% [markdown]
# ## 2. Consulta CONSTRUCT
Las consultas SELECT y CONSTRUCT tienen en común que hay un patrón de búsqueda en WHERE que produce una tabla intermedia de concordancias con N columnas (tantas como variables en el patrón) y filas _(?var1,...,?varN)=(valor1,...,valorN)_. En la siguiente consulta, cuando se aplica sobre el grafo anterior, una de esas concordancias es _(Extremadura, Badajoz_prov, Mérida)_.

En las consultas SELECT, desde cada una de estas N-tuplas se produce la construcción de uno de los resultados finales (una M-tupla) siguiendo las instrucciones en SELECT. Usualmente estas suponen escoger sólo algunas columnas determinadas (M de N) de esa tabla intermedia, pero hay otras opciones utilizables.


# %%
consulta1 = '''
PREFIX ej: <http://uned.es/ejs/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


CONSTRUCT {
   ej:Municipio rdf:type rdfs:Class .
   
   ?munic rdf:type ej:Municipio .  
   ?munic ej:en_comunidad ?comunid .
}
WHERE {
  ?comunid ej:tiene_provincia ?prov .
  ?prov ej:tiene_municipio ?munic .
}
'''

# %% [markdown]
**En estas consultas CONSTRUCT**, cada fila de la tabla intermedia de concordancias se utiliza para rellenar un patrón de grafo expresado en CONSTRUCT. En este ejemplo, los valores de la  fila _(?comunid, ?prov, ?munic)=(Extremadura, Badajoz_prov, Mérida)_ se utilizan para generar las siguientes tripletas del grafo resultante:
#
# ```
# ej:Municipio rdf:type rdfs:Class .
# ej:Mérida rdf:type ej:Municipio .  
# ej:Mérida ej:en_comunidad ej:Extremadura .
# ```
# Como el patrón en WHERE, en este ejemplo, genera una tabla de concordancias con 4 filas, el anterior conjunto de tripletas se repite 4 veces, para los respectivos valores de cada una de esas filas. El grafo resultante de la consulta resulta ser todo este conjunto de ternas incrementalmente creado. Conviene resaltar que la terna _(ej:Municipio, rdf:type, rdfs:Class_ se genera repetidamente para cada fila de la tabla de concordancias, pero una vez añadida al grafo resultante no se duplica.


# %% [markdown]
# ## 3. Ejecución y estructura de resultados

# %%
resp1_const = g_orig.query(consulta1)

# %% [markdown]
# El método `.query` permite indistintamente ejecutar una consulta de tipo SELECT o CONSTRUCT. Y el resultado devuelto tiene la misma estructura en ambos casos: un conjunto de tuplas. El siguiente bucle devolvería, una a una, las tuplas de estos resultados, provengan de una consulta SELECT o CONSTRUCT

# %% 
print(f"resp1_const es un objeto de tipo {type(resp1_const)} con las siguientes tuplas:")
for resp in resp1_const:
    print(resp)

# %% [markdown]
# En el caso de una consulta SELECT, estas tuplas pueden tener N componentes. Y en el caso de una consulta CONSTRUCT, los resultados siempre son 3-tuplas, tripletas. Por ello se pueden recorrer especificamente con el siguiente bucle sobre 'sujeto, predicado, objeto':

# %%
for s,p,o in resp1_const:
    print(s,p,o)


# %% [markdown]
# ## 4. Grafo resultante y visualización
# Los resultados obtenidos en `resp_const` son las tripletas del grafo resultante pero no se encuentran en una estructura reconocida en rdflib como un grafo sino en un iterador genérico de N-tuplas. El siguiente bucle va añadiendo a un nuevo grafo `g_const` una a una las tripletas (s,p,o) del resultado de las consulta CONSTRUCT:

# %%
g1_const = rdflib.Graph()
for s,p,o in resp1_const:
    g1_const.add((s,p,o))

# %% [markdown]
# Y este nuevo grafo (con los resultados) se puede visualizar con el siguiente procedimiento (o cualquier reescritura equivalente):

# %%
sio1 = StringIO()
rdf2dot(g1_const, sio1)
dot_source1 = sio1.getvalue()

gv1_const = graphviz.Source(dot_source1)
gv1_const 

# %% [markdown] 
# ## 5. Modificación del espacio de nombres
# El patrón del grafo que se desea, en `CONSTRUCT {...}`, puede directamente definir nuevos nodos y enlaces con espacios de nombres (prefijos) distintos al grafo consultado. O bien producirlos por alguna transformación sintática a partir de los originales.

# %%
consulta2 = '''
PREFIX ej: <http://uned.es/ejs/>
PREFIX otro: <http://otro.uned.es/ejs/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


CONSTRUCT {
   otro:Municipio rdf:type rdfs:Class .
   
   ?munic rdf:type otro:Municipio .  
   ?munic otro:en_comunidad ?comunid .
}
WHERE {
  ?comunid ej:tiene_provincia ?prov .
  ?prov ej:tiene_municipio ?munic .
}
'''

# %%
resp2_const = g_orig.query(consulta2)

g2_const = rdflib.Graph()
for s,p,o in resp2_const:
    g2_const.add((s,p,o))

g2_const_turtle = g2_const.serialize(format="turtle")
print(g2_const_turtle)

# %% [markdown]
# En este segundo ejemplo el grafo resultante introduce nodos y enlaces nuevos como _'Municipio'_ o _'en_comunidad'_ y se ha escogido construir su URL con un prefijo distinto al usado en el grafo original. 
#
#También es posible en el patrón en CONSTRUCT{...} aprovechar concordancias de municipio como _'http://uned.es/ejes/Mérida'_ para redefinir su URL resultante con otro prefijo. Este proceso de búsqueda y sustitución se produce en esta tercer consulta:

# %%
consulta3 = '''
PREFIX ej: <http://uned.es/ejs/>
PREFIX nuevo: <http://nuevo.uned.es/ejs/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
   nuevo:Municipio rdf:type rdfs:Class .
   
   ?munic_transf rdf:type nuevo:Municipio .  
   ?munic_transf nuevo:en_comunidad ?comunid .
}
# El patrón WHERE devuelve una columna adicional ?munic_transf construida a partir de ?munic
WHERE {
  ?comunid ej:tiene_provincia ?prov .
  ?prov ej:tiene_municipio ?munic .
  
  BIND( 
    IRI( 
      REPLACE( 
        STR(?munic),
        "^http://uned.es/ejs/",
        "http://transformado.uned.es/ejs/" 
      )
    ) 
    AS ?munic_transf 
  ) .
}
'''

# %% [markdown]
# Ejecución de la consulta3

# %%
resp3_const = g_orig.query(consulta3)

# %% [markdown]
# Impresión del grafo RDF resultante

#%%
g3_const = rdflib.Graph()
for s,p,o in resp3_const:
    g3_const.add((s,p,o))
    print(s,p,o)

# %% [markdown]
# Visualización del grafo resultante

# %%
sio3 = StringIO()
rdf2dot(g3_const, sio3)
dot_source3 = sio3.getvalue()

gv3_const = graphviz.Source(dot_source3)
gv3_const 
