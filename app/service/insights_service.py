from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

from utils.generation_calc import calc_inverters_generation, TimeSeriesValue

from model.medicao_model import MedicaoModel
from model.inversor_model import InversorModel



@dataclass
class InversorComPotencia:
    power: list[TimeSeriesValue]


def gerar_por_inversor(inversor_id: int, data_inicio: str, data_fim: str) -> float:
    dt_inicio = datetime.fromisoformat(data_inicio)
    dt_fim = datetime.fromisoformat(data_fim)

    registros = MedicaoModel.buscar_por_inversor_e_periodo(inversor_id, dt_inicio, dt_fim)

    serie = [
        TimeSeriesValue(value=potencia, date=data)
        for data, potencia in registros
        if potencia is not None
    ]

    entidade = InversorComPotencia(power=serie)

    return calc_inverters_generation([entidade])

def gerar_por_usina(usina_id: int, data_inicio: str, data_fim: str) -> float:
    dt_inicio = datetime.fromisoformat(data_inicio)
    dt_fim = datetime.fromisoformat(data_fim)

    inversores = InversorModel.listar_por_usina(usina_id)
    entidades = []

    for inversor_id in inversores:
        registros = MedicaoModel.buscar_por_inversor_e_periodo(inversor_id, dt_inicio, dt_fim)

        serie = [
            TimeSeriesValue(value = potencia, date = data)
            for data, potencia in registros
            if potencia is not None
        ]
    if len(serie) >= 2:
        entidades.append(InversorComPotencia(power = serie))

    return calc_inverters_generation(entidades)

def potencia_maxima_por_dia(inversor_id: int, data_inicio: str, data_fim: str) -> dict:
    dt_inicio = datetime.fromisoformat(data_inicio)
    dt_fim = datetime.fromisoformat(data_fim)

    registros = MedicaoModel.listar_potencias_por_inversor(inversor_id, dt_inicio, dt_fim)

    potencia_por_dia = defaultdict(list)

    for data_hora, potencia in registros:
        dia = data_hora.date() # extrai só a data
        potencia_por_dia[dia].append(potencia)

    resultado = {
        str(dia): max(valores)
        for dia, valores in potencia_por_dia.items()
    }

    return resultado

def temperatura_media_por_dia(inversor_id: int, data_inicio: str, data_fim: str) -> dict:
    dt_inicio = datetime.fromisoformat(data_inicio)
    dt_fim = datetime.fromisoformat(data_fim)

    registros = MedicaoModel.listar_temperaturas_por_inversor(inversor_id, dt_inicio, dt_fim)

    temperaturas_por_dia = defaultdict(list)

    for data_hora, temperatura in registros:
        dia = data_hora.date()
        temperaturas_por_dia[dia].append(temperatura)
    
    resultado = {
        str(dia): sum(valores) / len(valores)
        for dia, valores in temperaturas_por_dia.items()
        if valores
    }

    return resultado