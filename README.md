# PokedexDB - Projeto de Engenharia de Dados

Este projeto tem como objetivo criar um **data pipeline simplificado** para armazenar dados da PokéAPI em um banco MySQL local, simulando um **Data Lake / Raw Layer**. 

OBS.: Estou em processo de aprendizagem com o README, tudo aqui foi escrito com auxilio ou quase inteiramente por inteligência artificial (ChatGPT).

---

## Estrutura do Projeto

- config/
  - db_config.json        # Configurações de acesso ao MySQL
- src/
  - load_pokemon.py       # Script para buscar Pokémon da API e inserir no banco
- venv/                   # Ambiente virtual Python (ignorando no git)
- .gitignore
- requirements.txt
- README.md


## Tecnologias

- Python 3
- PyMySQL
- Requests
- MySQL
- JSON (armazenamento de dados semi-estruturados)

---

## Banco de Dados

### Tabela `pokemons_raw`

| Coluna      | Tipo       | Descrição |
|------------|-----------|-----------|
| id         | INT       | ID oficial do Pokémon (PK, da PokéAPI) |
| name       | VARCHAR   | Nome do Pokémon |
| raw_data   | JSON      | JSON completo retornado da PokéAPI |
| created_at | TIMESTAMP | Timestamp de inserção (automático) |

Exemplo de criação da tabela:

```sql
CREATE TABLE pokemons_raw (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    raw_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Funcionalidades
Conexão com a PokéAPI

Armazenamento do JSON completo em MySQL

Evita duplicação usando ON DUPLICATE KEY UPDATE

Fácil expansão futura: ETL para criar tabelas analíticas, rankings, etc.

Como Rodar
Crie o ambiente virtual:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
Instale dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Configure o banco no config/db_config.json:

json
Copiar
Editar
{
  "host": "localhost",
  "user": "seu_usuario",
  "password": "sua_senha",
  "database": "pokedexdb"
}
Rode o script para carregar um Pokémon:

bash
Copiar
Editar
python src/load_pokemon.py
Observações
Atualmente o pipeline pega um Pokémon por vez.

Coluna raw_data pode ser gigante; recomenda-se usar queries específicas ou JSON_EXTRACT para não travar o terminal.

Futuramente, o pipeline será automatizado para ingestão diária de novos Pokémon.

Próximos Passos
Automatizar ingestão incremental

Criar tabelas analíticas para ranking de stats

Suportar diferentes formas/variações de Pokémon