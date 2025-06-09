# %% [markdown]
# [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jlfvindel/grafos_RDF/blob/main/1_Gestion_SPARQL/1e-grafo_local-administracion.ipynb)

# %% [markdown]
# # Gestión mediante SPARQL: borrado e inserción


# %% [markdown]
# ## Resumen del cuaderno
# 1. En SPARQL se pueden formular instrucciones de inserción de tripletas, de borrado de tripletas o combinadas de borrado/inserción.
# 2. Este borrado o inserción puede ser absoluto (facilitando todos los componentes de la tripleta afectada) o bien se pueden ejecutar de forma relativa a partir de concordancias encontradas en un patrón de búsqueda WHERE.

En el documento [SPARQL QUERY](https://www.w3.org/TR/sparql11-update/) se detalla el diseño de consultas SELECT y CONSTRUCT (además de consultas ASK y DESCRIBE, menos usadas). En el documento [SPARQL UPDATE](https://www.w3.org/TR/2013/REC-sparql11-query-20130321/) se detalla el diseño de patrones INSERT y DELETE.

# %% [markdown]
# ## 1 Grafo original

# %%
!pip install rdflib

# %%
import rdflib

g = rdflib.Graph()

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

g.parse(data=txt_turtle, format="turtle")

# %%
from rdflib.tools.rdf2dot import rdf2dot
from io import StringIO
import graphviz

# %% [markdown]
# ## 1.1 Visualización del grafo original
# Para facilitar sucesivas llamadas a este procedimiento, se define la siguiente función:

# %%
def visualiza(grafo):
    sio = StringIO()
    rdf2dot(grafo,sio)
    return (graphviz.Source(sio.getvalue()))

# %%
visualiza(g)


# %% [markdown]
# ## 2. Borrado e inserción
# ### 2.1 Inserción directa de tripletas

# La inserción de una o más tripletas se produce como sigue. Conviene resaltar que ya no se usa el método `.query()` sino el método `.update()`.

# %%
admin1 = """
PREFIX ej: <http://uned.es/ejs/> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 


INSERT DATA {
  ej:Cáceres_prov ej:tiene_municipio ej:Trujillo .
  ej:Trujillo rdf:type ej:Municipio .
}
"""

# %%
g.update(admin1)
visualiza(g)

# %% [markdown]
# ### 2.2 Borrado directo de tripletas

# %%
admin2 = """
PREFIX ej: <http://uned.es/ejs/> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 


DELETE DATA {
  ej:Trujillo rdf:type ej:Municipio .
}
"""

# %%
g.update(admin2)
visualiza(g)

# %% [markdown]
# ### 2.3 Borrado y/o inserción de tripletas localizadas
# En este punto, el patrón en WHERE encuentra 5 concordancias (tres pueblos de Cáceres_prov y dos de Badajoz_prov). Para cada una de estas concordancias _(?prov,?munic)_ se ejecuta el borrado en DELETE y la inserción en INSERT. Este esquema se puede usar sólo con inserción o sólo con borrado (omitiendo la otra instrucción).

# %%
admin3 = """
PREFIX ej: <http://uned.es/ejs/> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

DELETE {
  ?prov ej:tiene_municipio ?munic .
}
INSERT {
  ?munic ej:en_provincia ?prov .
  ?munic rdf:type ej:Municipio .
}
WHERE {
  ?prov ej:tiene_municipio ?munic .
}
"""

# %%
g.update(admin3)
visualiza(g)

# %% [markdown]
# ## 3. Sobre el uso de gestores de bases de datos RDF
# Todos los cuadernos de esta sección instancian grafos en memoria y los pueblan, consultan, exportan y administran a través de instrucciones SPARQL facilitadas a los métodos `.parse()`, `.query()`, `.serialize()` o `.update()`. De esta forma se puede gestionar una sencilla base de ternas RDF con permanencia basada en ficheros.
#
# Alternativamente hay gestores RDF con interfaz gráfico que simplifican mucho estas tareas de consulta y administración, así como la navegación filtrada y por pasos sobre la representación visual del grafo. [GraphDB](https://graphdb.ontotext.com/documentation/11.0/userroles.html#role-everyone) es uno de estos gestores y facilita un editor de instrucciones SPARQL ejecutable sobre el grafo seleccionado.