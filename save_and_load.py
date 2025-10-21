import json


def salvar(conteudo, arquivo="saving"):
    with open(f"data/{arquivo}.json", "w", encoding='utf-8') as saving:
        json.dump(conteudo, saving)

def carregar(arquivo="saving") -> dict:
    with open(f"data/{arquivo}.json", encoding='utf-8') as loading:
        data = json.load(loading)
        return data
    