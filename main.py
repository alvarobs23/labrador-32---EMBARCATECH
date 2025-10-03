import os
import time
from datetime import datetime
from periphery import I2C

# Interval (segundos)
INTERVAL_SEC = 1

# Path (pasta que simula o SD card)
SD_CARD = "/home/caninos/SD_CARD"
DATALOGGER = "/data.txt"

# AHT10 config (usar I2C-3)
I2C_BUS = "/dev/i2c-3"
I2C_ADDRESS = 0x38

# cria pasta simulando SD se não existir
os.makedirs(SD_CARD, exist_ok=True)

# inicializa I2C (abre o device)
try:
    i2c = I2C(I2C_BUS)
except Exception as e:
    print(f"Erro ao abrir {I2C_BUS}: {e}")
    raise SystemExit(1)


def aht10_init():
    """
    Inicializa AHT10.
    """
    init_command = [0xBE, 0x08, 0x00]
    i2c.transfer(I2C_ADDRESS, [I2C.Message(init_command)])
    time.sleep(0.5)


def aht10_measure():
    """
    Envia comando de medição ao AHT10.
    """
    measure_command = [0xAC, 0x33, 0x00]
    i2c.transfer(I2C_ADDRESS, [I2C.Message(measure_command)])
    time.sleep(0.5)


def aht10_read():
    """
    Lê 6 bytes do AHT10 e retorna os dados.
    """
    read_command = I2C.Message([0x00] * 6, read=True)
    i2c.transfer(I2C_ADDRESS, [read_command])
    return read_command.data


def aht10_data(data):
    """
    Converte os 6 bytes em umidade (%) e temperatura (°C).
    """
    # segurança: verificar comprimento
    if len(data) < 6:
        raise RuntimeError("Leitura AHT10 incompleta")

    humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / (1 << 20)
    temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / (1 << 20) - 50
    return humidity, temperature


def main():
    print("Iniciando monitoramento!\n")

    # escreve cabeçalho com unidades (tenta criar arquivo novo)
    header = "data_hora(AAAA-MM-DD HH:MM:SS),umidade(%),temperatura(°C)\n"
    try:
        with open(SD_CARD + DATALOGGER, "x") as f:
            f.write(header)
    except FileExistsError:
        print("Arquivo já existe. Novos dados serão acrescentados.\n")

    # inicia sensor
    aht10_init()

    print(header.strip()) # mostra cabeçalho no terminal

    try:
        while True:
            # timestamp sem microssegundos
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # leitura AHT10
            aht10_measure()
            data = aht10_read()
            hum, temp = aht10_data(data)

            # formata saída com unidades
            line_print = f"{timestamp},{hum:.2f} %,{temp:.2f} °C"
            print(line_print)

            # grava no arquivo
            with open(SD_CARD + DATALOGGER, "a") as f:
                f.write(line_print + "\n")

            time.sleep(INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Finalizando monitoramento...\n")
    except Exception as e:
        print(f"\nErro durante o monitoramento: {e}\n")
    finally:
        try:
            i2c.close()
        except Exception:
            pass
        print("I2C fechado. Saindo.")


if __name__ == "__main__":
    main()
