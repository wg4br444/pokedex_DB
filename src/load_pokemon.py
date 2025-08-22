import json
import requests
import pymysql

#Configs para acessar o banco
with open("/home/gabriel/Documentos/pokedex_DB/config/db_config.json") as f:
    config = json.load(f)

#Function para encontrar o pokemon
def get_pokemon(name: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
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

try:

    #Aqui futuramente vou automatizar ou criar interação para que busque sem alterar o código toda vez
    pokemon = get_pokemon("Flygon")

    #Extrai dados exigidos na table pokemon_raw
    poke_id = pokemon["id"]
    poke_name = pokemon["name"]
    raw_json = json.dumps(pokemon)

    #Insert no banco
    sql = """
        INSERT INTO pokemons_raw (id, name, raw_data)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            name = VALUES(name), 
            raw_data = VALUES(raw_data)
    """
    cursor.execute(sql, (poke_id, poke_name, raw_json))
    connection.commit()

    print(f"{poke_name.capitalize()} inserido/atualizado com sucesso!")

except Exception as e:
    print(f"Erro: {e}")

finally:
    cursor.close()
    connection.close()
