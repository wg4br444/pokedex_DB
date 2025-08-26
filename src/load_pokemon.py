import json
import requests
import pymysql

#Configs para acessar o banco
with open("/home/gabriel/Documentos/pokedex_DB/config/db_config.json") as f:
    config = json.load(f)

#Função para buscar Pokémon por nome ou ID
def get_pokemon(identifier):
    url = f"https://pokeapi.co/api/v2/pokemon/{identifier}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

#Conectar no MySQL
connection = pymysql.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"],
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

#Quantos Pokemons vamos trazer por vez?
N = 5

try:
    #Pega o último ID inserido
    cursor.execute("SELECT MAX(id) as last_id FROM pokemons_raw")
    result = cursor.fetchone()
    last_id = result["last_id"]

    #Se a tabela estiver vazia, começa do #1
    if last_id is None:
        next_id = 1
    else:
        next_id = last_id + 1

    #Loop que insere N Pokemons de acordo com definido acima
    for i in range(N):
        pokemon = get_pokemon(next_id)

        poke_id = pokemon["id"]
        poke_name = pokemon["name"]
        raw_json = json.dumps(pokemon)

        sql ="""
            INSERT INTO pokemons_raw (id, name, raw_data)
            VALUES (%s, %s, %s)
            """
        cursor.execute(sql, (poke_id, poke_name, raw_json))
        connection.commit()

        print(f"{poke_name.capitalize()} (id={poke_id}) inserido/atualizado com sucesso!")

        next_id += 1  #Próximo Pokemon

except Exception as e:
    print(f"Erro: {e}")

finally:
    cursor.close()
    connection.close()
