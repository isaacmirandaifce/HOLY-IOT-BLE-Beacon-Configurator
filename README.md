# HOLY-IOT-BLE-Beacon-Configurator

Uma biblioteca Python leve e assíncrona para configuração de Beacons BLE (Bluetooth Low Energy) que utilizam o protocolo **UART Nordic**. Este projeto foi desenvolvido especificamente para facilitar a automação e configuração em lote de dispositivos Holy-IoT.

##  Funcionalidades

O configurador permite alterar os principais parâmetros do beacon via comandos GATT:

* **Autenticação:** Suporte a desbloqueio via senha hexadecimal.
* **Identificação:** Alteração de UUID, Major e Minor.
* **Personalização:** Mudança do nome de transmissão (até 12 caracteres).
* **Performance:** Ajuste de TX Power e Intervalo de Advertising.
* **Execução em Lote:** Estrutura assíncrona que permite configurar múltiplos dispositivos em sequência.

---

##  Pré-requisitos

Certifique-se de ter o Python 3.7+ instalado e a biblioteca `bleak` (Bluetooth Low Energy platform Agnostic Klient).

```bash
pip install bleak

```

---

##  Estrutura do Projeto

* `beacon_configurator.py`: O core da biblioteca contendo a classe `BeaconConfigurator`.
* `test_beacon_configurator.py`: Script de exemplo para homologação e testes rápidos.

---

##  Como Usar

### 1. Configuração Básica

Importe a classe e defina o endereço MAC do seu dispositivo. Você pode escolher quais parâmetros deseja alterar; os que não forem informados permanecerão com os valores atuais do dispositivo.

```python
from beacon_configurator import BeaconConfigurator
import asyncio

async def main():
    # Inicializa o beacon pelo MAC Address
    beacon = BeaconConfigurator("E4:A1:80:DD:40:57")
    
    # Configura os parâmetros desejados
    await beacon.configure(
        password_hex="aa14061112", # Senha de acesso
        name="MeuBeacon01",        # Nome customizado
        major=100,
        minor=50
    )

if __name__ == "__main__":
    asyncio.run(main())

```

### 2. Parâmetros Suportados

| Parâmetro | Tipo | Descrição |
| --- | --- | --- |
| `password_hex` | String | Senha em formato hexadecimal (ex: "123456"). |
| `uuid` | String | Novo UUID para o iBeacon. |
| `major` | Integer | Valor Major (0-65535). |
| `minor` | Integer | Valor Minor (0-65535). |
| `name` | String | Nome de até 12 caracteres. |
| `tx_power` | Integer | Potência de transmissão em dBm. |
| `adv_interval` | Integer | Índice do intervalo de advertising. |

---

##  Protocolo de Comunicação

A biblioteca comunica-se através do UUID de serviço UART da Nordic:

* **UART RX UUID:** `6e400002-b5a3-f393-e0a9-e50e24dcca9e`
* **Magic Byte:** `0xF3`

Cada pacote é construído dinamicamente seguindo a estrutura:
`[MAGIC_BYTE] [CMD_ID] [MAGIC_BYTE] [LENGTH] [DATA_BYTES]`

---

##  Notas Importantes

* **Distância:** Certifique-se de que o beacon está próximo ao computador durante a configuração para evitar falhas de escrita.
* **Permissões:** Em sistemas Linux, pode ser necessário executar o script com privilégios de `sudo` ou configurar as permissões do adaptador Bluetooth.
