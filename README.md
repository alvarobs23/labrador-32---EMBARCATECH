# Registrador de dados AHT10

O projeto implementa um datalogger de temperatura e umidade no SBC Labrador 32 usando o sensor AHT10.

## Instruções

### 1. Crie um ambiente virtual.
```bash
python3 -m venv .venv
```

### 2. Ative o ambiente virtual.
```bash
source .venv/bin/activate
```

### 3. Instale as dependências.
```bash
pip install -r requirements.txt
```

### 4. Configure as permissões I2C.
```bash
sudo chown caninos /dev/i2c-3
sudo chmod g+rw /dev/i2c-3
```

### 5. Altere os valores das variáveis se necessário.
```python
SD_CARD = "/home/caninos/SD_CARD"
DATALOGGER = "/data.txt"
```

### 6. Execute o programa.
Utilize-se o superusuário para simplificar o uso das permissões. No entanto, não é recomendado.
```bash
sudo $PWD/.venv/bin/python main.py
```

## Hardware Necessário

- **Placa Labrador 32** (Coreboard V2.x + Baseboard)
- **Sensor AHT10** (temperatura e umidade)
- **Cartão microSD** (mínimo 4GB)

## Conexões do Sensor AHT10

| Pino AHT10 | Pino Labrador 32 | Função |
|------------|------------------|---------|
| VCC        | 3.3V             | Alimentação |
| GND        | GND              | Terra |
| SDA        | GPIOC27 (I2C-3)    | Dados I2C |
| SCL        | GPIOC26 (I2C-3)    | Clock I2C |

## Configurações

### Parâmetros ajustáveis no `main.py`:
```python
# Intervalo entre medições (segundos)
INTERVAL_SEC = 1

# Caminho do arquivo de log
SD_CARD = "/home/caninos/SD_CARD"
DATALOGGER = "/data.txt"

# Configuração I2C
I2C_BUS = "/dev/i2c-3"      # Bus I2C-3
I2C_ADDRESS = 0x38          # Endereço do AHT10
```

### Formato do arquivo de log:
```
data_hora(AAAA-MM-DD HH:MM:SS),umidade(%),temperatura(°C)
2024-01-15 10:30:00,45.23 %,23.45 °C
2024-01-15 10:30:01,45.25 %,23.47 °C
```

## Troubleshooting

### Problema: "Erro ao abrir /dev/i2c-3"
```bash
sudo chown caninos /dev/i2c-3
sudo chmod g+rw /dev/i2c-3
```

### Problema: "ModuleNotFoundError: No module named 'periphery'"
```bash
pip3 install python-periphery
```

### Problema: Sensor não detectado
```bash
i2cdetect -y 3
# Deve mostrar 0x38 na saída
```

---

**Desenvolvido para a placa Labrador 32 da Caninos Loucos** 🐕


