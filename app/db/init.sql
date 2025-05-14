CREATE TABLE IF NOT EXISTS usina (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS inversor (
    id INTEGER PRIMARY KEY,
    usina_id INTEGER NOT NULL,
    FOREIGN KEY (usina_id) REFERENCES usina(id)
);

CREATE TABLE IF NOT EXISTS medicao (
    id SERIAL PRIMARY KEY,
    inversor_id INTEGER NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    potencia_ativa_watt REAL,
    temperatura_celsius REAL,
    FOREIGN KEY (inversor_id) REFERENCES inversor(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_medicao_inversor_data
ON medicao (inversor_id, data_hora);
