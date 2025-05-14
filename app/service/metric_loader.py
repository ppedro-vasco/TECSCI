import json

from pathlib import Path

from model.medicao_model import MedicaoModel
from dto.medicao_dto import MedicaoDTO

def carregar_metrics(caminho_arquivo=None):
    if caminho_arquivo is None:
        caminho_arquivo = Path(__file__).parent.parent / "static" / "metrics.json"
    
    if not Path(caminho_arquivo).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return

    inseridos = 0
    for item in dados:
        dto = MedicaoDTO.from_dict(item)
        if dto:
            MedicaoModel.inserir(
                inversor_id=dto.inversor_id,
                data_hora=dto.data_hora,
                potencia=dto.potencia_ativa,
                temperatura=dto.temperatura
            )
            inseridos += 1
        else:
            print(f"Registro inválido ignorado: {item}")

        print(f"{inseridos} medições inseridas com sucesso.")