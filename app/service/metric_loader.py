import json

from pathlib import Path
from datetime import datetime

from model.medicao_model import MedicaoModel

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
        try:
            MedicaoModel.inserir(
                inversor_id=int(item["inversor_id"]),
                data_hora=datetime.fromisoformat(item["datetime"]["$date"].replace("Z", "+00:00")),
                potencia=float(item["potencia_ativa_watt"]),
                temperatura=float(item["temperatura_celsius"])
            )
            inseridos += 1
        except (KeyError, ValueError, TypeError) as e:
            print(f"Erro ao processar item: {item} → {e}")
            continue


    print(f"{inseridos} medições inseridas com sucesso.")