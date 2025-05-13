from service.insights_service import gerar_por_inversor
from service.insights_service import gerar_por_usina
from service.insights_service import potencia_maxima_por_dia
from service.insights_service import temperatura_media_por_dia

valor = gerar_por_inversor(
    inversor_id = 1,
    data_inicio = "2025-01-01T00:00:00",
    data_fim = "2025-01-31T23:59:59"
)

valor = gerar_por_usina(
    usina_id = 1,
    data_inicio = "2025-01-01T00:00:00",
    data_fim = "2025-01-31T23:59:59"
)

valores = potencia_maxima_por_dia(
    inversor_id = 1,
    data_inicio="2025-01-01T00:00:00",
    data_fim="2025-01-10T23:59:59"
)

print(f"Geração total do Inversor 1 em janeiro: {valor:.2f} Wh")

print(f"Geração total da Usina 1 em janeiro: {valor:.2f} Wh")

print("Potência máxima por dia (inversor 1):")
for dia, valor in valores.items():
    print(f"{dia}: {valor:.2f} W")

print("\nTemperatura média por dia (inversor 1):")
medias = temperatura_media_por_dia(
    inversor_id=1,
    data_inicio="2025-01-01T00:00:00",
    data_fim="2025-01-07T23:59:59"
)

for dia, temp in medias.items():
    print(f"{dia}: {temp:.2f} °C")