# %% [markdown]
# # Consultas SPARQL SELECT a un grafo local
#
# ## Resumen del cuaderno
# 1. **En general: consulta SPARQL a un grafo rdflib**. Mediante `resp1= g1.query(consulta1)` se puede interrogar un grafo `g1` en memoria con una consulta SPARQL almacenada en la variable `consulta1`. Los resultados se almacenan en `resp1`.
# 2. **Consulta SPARQL de tipo SELECT: devuelve una tabla de N-columnas**. La respuesta a una consulta `SELECT ?var1 var2 ... varN WHERE {...}` devuelve una tabla con 0 o más filas y con N columnas (una por cada varX).


# %% [markdown]
# ## 1. Declaración del grafo y de la consulta 

# %% [markdown]
# ### 1.1 Grafo consultado

# %%
import rdflib

g1 = rdflib.Graph()

# %%
# Provincias de la Comunidad Valenciana, con algunos de sus municipios
txt_turtle = '''
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
g1.parse(data=txt_turtle, format='turtle')

# %% [markdown]
# Visualización del grafo

# %%
from rdflib.tools.rdf2dot import rdf2dot
from io import StringIO
import graphviz

sio1 = StringIO()
rdf2dot(g1, sio1)
dot_source1 = sio1.getvalue()
gv1 = graphviz.Source(dot_source1)
gv1  

# %% [markdown]
# ### 1.2 Consulta SPARQL SELECT
#
# **Patrón de consulta en WHERE**. Se puede resumir como `?comunid --tiene_provincia--> ?prov --tiene_municipio--> ?munic`. Una comunidad concreta tiene asignada una provincia concreta y ésta a su vez tiene asignado un municipio concreto. En el grafo anterior, una concordancia se encuentra para _(?comunid,?prov,?munic)=(Comunidad_Valenciana,Alicante_prov,Elche)_. Otra concordancia se encuentra en _(Comunidad_Valenciana,Alicante_prov,Alicante_munic)_.  
#
# **Tabla de concordancias del patron**. Hay un total de 6 concordancias encontradas y cada una es una 3-tupla porque aparecían 3 variables en el patrón de consulta. En general, para un patrón de consulta con N variables, se genera una tabla intermedia de resultados con N columnas. En este caso, donde aparecen 3 variables (?var) en el patrón de consulta, la tabla de concordancias se compone de 3-tuplas como las siguientes:
#
# | ?comunid | ?prov  |  ?munic |
# | :------: | :----: | :-----: |
# | ej:Comunidad_Valenciana | ej:Alicante_prov | ej:Elche |
# | ....... | ....... | ....... |

# %%
consulta1 = '''
PREFIX ej: <http://uned.es/ejs/>

SELECT ?munic ?comunid
WHERE {
  ?comunid ej:tiene_provincia ?prov .
  ?prov ej:tiene_municipio ?munic .
}
'''

# %% [markdown]
# **Tablas final de resultados devueltos por la consulta**. En `SELECT ?munic ?comunid` se indica que tan sólo se quieren esas dos columnas de las tres que presenta la tabla intermedia de resultados y además en ese orden. Es decir, una fila de la tabla de resultados finales puede ser *(Elche, Comunidad_Valenciana)* y otra podría ser *(Alicante_munic, Comunidad_Valenciana)*. Hay un total de 6 resultados finales y todos son 2-tuplas.

# %% [markdown]
# ### 1.3 Almacenamiento opcional de la consulta
# Es una buena práctica salvar las diversas consultas aplicables a un grafo en distintos ficheros, para ser utilizadas posteriormente sin tener que reescribirlas.

# %%
# En caso de que el subdirectorio fichs no existiera, lo crea.
import os
ruta_consulta1 = "fichs/1c-munic_comunid.sparql"
os.makedirs(os.path.dirname(ruta_consulta1), exist_ok=True)

# La pregunta se escribe como texto plano, preferiblemente en formato utf-8
with open(ruta_consulta1, "w", encoding="utf-8") as f:
    f.write(consulta1)

# %% [markdown]
# ## 2. Ejecución de la consulta 
# La ejecución de esta `consulta1` sobre un grafo denominado `g` se ejecuta como sigue.

# %%
resp1 = g1.query(consulta1)

# %% [markdown]
# ## 3. Estructura de la tabla resultante 

# %% [markdown]
# ### 3.1 Cabecera de la tabla
# La variable `resp1` recoge en este caso un conjunto de seis 2-tuplas, con los valores de las diversas concordancias para `(?munic, ?comunid)`. Estas dos variables demandadas en SELECT se encuentran almacenadas en `resp1.vars`.

# %%
print('Cabecera de la tabla: variables escogidas en la consulta SELECT en el mismo orden en que figuran en la consulta')    
print(resp1.vars)

# %% [markdown]
# ### 3.2 Filas presentadas de forma autocontenida
# %% [markdown]
# **Filas devueltas por la consulta SELECT (en forma de diccionario)**. De esta tabla de 6 filas en dos columnas, el método `resp1.bindings` presenta cada fila en forma de diccionario: {?munic: valor_munic, ?comunid: valor_comunid}. Para imprimirlas de forma separada, se recorren una a una estas filas.

# %%
print('Listado de respuestas de la consulta SELECT, en forma de diccionarios que describen cada fila:')
for fila in resp1.bindings:
    print(fila)

# %% [markdown]
# ### 3.2 Filas presentadas respecto a cabeceras
# %% [markdown]
#
# **Filas devueltas por la consulta SELECT (en forma de tuplas)**. La siguiente impresión presenta las filas de la tabla como 2-tuplas, sin referencia a la cabecera de su respectiva columna. En este caso, el orden de estas tuplas es el mismo que el de la tupla de las cabeceras mostrado en `resp1.vars`.

# %%
print('Listado de respuestas de la consulta SELECT, en forma de tuplas (con cabeceras implícitas respecto a resp.vars):')
for fila in resp1:
      print(fila)

# %% [markdown]
# ## 4. Tabla resultante presentada mediante Pandas

# %% [markdown]
# Pandas es el paquete más utilizado en Python para la presentación y análisis de datos tabulares.

# %%
import pandas as pd

# %% [markdown]
# Una tabla Pandas es una instancia de DataFrame. Para inicializar esta instancia hay que facilitar la lista de literales de las cabeceras y la lista de las filas que contendrá, que en este ejemplo son respectivamente `resp.vars` y `resp`. 

# %%
cabeceras = resp1.vars
rows = resp1

df = pd.DataFrame(rows, columns=cabeceras)
display(df)

# %% [markdown]
# ### 4.1 Exportación del DataFrame
# Un DataFrame de Pandas es una tabla y se puede exportar en los diferentes formatos en que se almacenan datos tabulares (CSV, etc).

# %%
# 1. CSV
df.to_csv('fichs/1c-sparql_select-resp1.csv', sep=';', encoding='utf-8', index=False)

# 2. Excel
df.to_excel('fichs/1c-sparql_select-resp1.xlsx', sheet_name='Resultados', index=False)

# 3. JSON (una línea por registro)
df.to_json('fichs/1c-sparql_select-resp1.json', orient='records', lines=True)

# %% [markdown]
# ## 5. Ficheros con grafos y con consultas
# El grafo consultado se podia haber cargado desde un fichero así como la consulta aplicable al grafo. En esta seccion:
# 1. Se rescata un fichero generado en otro cuaderno con las provincias de la Comunidad Valencia y de Extremadura y dos municipios por provincia.
# 2. Se rescata el fichero donde se exportó la _'consulta1'_ en una nueva variable _'consulta2'_, como si no se hubiera declarado al inicio de este cuaderno y sólo se dispusiera de ella desde un fichero. 

# %% [markdown]
# ### 5.1 Carga del grafo desde un fichero

# %%
ruta_grafo = "fichs/1a-comunid_prov_munic.ttl"
g2 = rdflib.Graph()

try:
    # Antes de parsear, verificamos si el fichero RDF existe en disco
    if not os.path.exists(ruta_grafo):
        raise FileNotFoundError(f"No se encontró el fichero en: {ruta_grafo}")
    
    # Si existe, lo parseamos. Si se omite el formato en el método _parse_ trata de detectarlo por extensión o por contenido.
    g2.parse(ruta_grafo, format="turtle")
    
    print(f"Grafo cargado correctamente. Contiene {len(g2)} tripletas.")
    print(g2.serialize(format="turtle"))

except FileNotFoundError as fnf:
    print(f"Error: {fnf}")

# %% [markdown]
# ### 5.2 Carga de la consulta desde un fichero

# %%
ruta_consulta2 = "fichs/1c-munic_comunid.sparql"
try:
    if not os.path.exists(ruta_consulta2):
        # Si la ruta no existe, lanzamos un error
        raise FileNotFoundError(f"No se encontró el fichero de consulta: {ruta_consulta2}")
    
    # Si existe, lo abrimos y leemos todo su contenido
    with open(ruta_consulta2, "r", encoding="utf-8") as f:
        consulta2 = f.read()
    print(consulta2)    

except FileNotFoundError as fnf:
    print(f"Error: {fnf}")

# %% [markdown]
# ### 5.3 Ejecución de la consulta sobre el grafo

# %%
resp2 = g2.query(consulta2)

# %%
# Resultados, presentados en un DataFrame de Pandas
df2 = pd.DataFrame(resp2, columns=resp2.vars)
display(df)

