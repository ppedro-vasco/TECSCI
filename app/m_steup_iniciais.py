from model.usina_model import UsinaModel
from model.inversor_model import InversorModel

usina1_id = UsinaModel.criar("Usina 1")
usina2_id = UsinaModel.criar("Usina 2")

for inversor_id in range(1, 5):
    InversorModel.criar(inversor_id, usina1_id)

for inversor_id in range(5, 9):
    InversorModel.criar(inversor_id, usina2_id)

print("Dados iniciais inseridos com sucesso.")
