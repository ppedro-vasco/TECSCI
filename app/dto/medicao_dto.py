from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MedicaoDTO:
    inversor_id: int
    data_hora: datetime
    potencia_ativa: float
    temperatura: float

    @staticmethod
    def from_dict(data: dict) -> Optional["MedicaoDTO"]:
        """
        Cria uma instância de MedicaoDTO a partir de um dicionário.
        Retorna None se os dados forem inválidos ou incompletos.
        """
        try:
            raw_datetime = data.get("datetime")
            if isinstance(raw_datetime, dict) and "$date" in raw_datetime:
                data_str = raw_datetime["$date"].replace("Z", "+00:00")
                data_hora = datetime.fromisoformat(data_str)
            else: 
                return None
            
            potencia = data.get("potencia_ativa_watt")
            temperatura = data.get("temperatura_celsius")

            if potencia is None or temperatura is None:
                return None
            
            return MedicaoDTO(
                inversor_id=int(data["inversor_id"]),
                data_hora=data_hora,
                potencia_ativa=float(potencia),
                temperatura=float(temperatura)
            )
        
        except (KeyError, ValueError, TypeError):
            return None