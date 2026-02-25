import asyncio
import struct
from bleak import BleakClient

class BeaconConfigurator:
    """
    Biblioteca para configuração de Beacons BLE via protocolo UART Nordic.
    """
    
    # Constantes do Protocolo
    UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    MAGIC_BYTE = 0xF3

    CMD_PASSWORD     = 0x01
    CMD_UUID         = 0x02
    CMD_MAJOR        = 0x03
    CMD_MINOR        = 0x04
    CMD_NAME         = 0x05
    CMD_ADV_INTERVAL = 0x06
    CMD_TX_POWER     = 0x07
    CMD_RSSI_1M      = 0x08

    def __init__(self, mac_address):
        """
        Inicializa o configurador para um beacon específico.
        :param mac_address: Endereço MAC do dispositivo (ex: "E4:A1:80:DD:40:57")
        """
        self.mac_address = mac_address

    def _build_packet(self, cmd_id, data_bytes):
        """Monta o pacote binário no padrão exato do fabricante."""
        length = len(data_bytes)
        packet = bytearray([self.MAGIC_BYTE, cmd_id, self.MAGIC_BYTE, length])
        packet.extend(data_bytes)
        return packet

    async def configure(self, password_hex=None, uuid=None, major=None, minor=None, 
                        name=None, tx_power=None, adv_interval=None, delay_between_commands=1.0):
        """
        Conecta ao beacon e aplica todas as configurações fornecidas.
        Os parâmetros que forem passados como 'None' serão ignorados.
        """
        print(f"Tentando conectar ao beacon {self.mac_address}...")
        
        async with BleakClient(self.mac_address) as client:
            if not client.is_connected:
                print(f"[{self.mac_address}] Falha ao conectar.")
                return False
            
            print(f"[{self.mac_address}] Conectado! Iniciando envio das configurações...\n")

            try:
                # 1. Autenticação
                if password_hex:
                    print("Enviando senha de autenticação...")
                    password_bytes = bytes.fromhex(password_hex)
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_PASSWORD, password_bytes))
                    await asyncio.sleep(delay_between_commands)

                # 2. Alterar UUID
                if uuid is not None:
                    print(f"Alterando UUID para {uuid}...")
                    uuid_limpo = uuid.replace('-', '')
                    uuid_bytes = bytes.fromhex(uuid_limpo)
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_UUID, uuid_bytes))
                    await asyncio.sleep(delay_between_commands)

                # 3. Alterar Major
                if major is not None:
                    print(f"Alterando Major para {major}...")
                    major_bytes = struct.pack('>H', major)
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_MAJOR, major_bytes))
                    await asyncio.sleep(delay_between_commands)

                # 4. Alterar Minor
                if minor is not None:
                    print(f"Alterando Minor para {minor}...")
                    minor_bytes = struct.pack('>H', minor)
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_MINOR, minor_bytes))
                    await asyncio.sleep(delay_between_commands)

                # 5. Alterar Nome
                if name is not None:
                    print(f"Alterando Nome para '{name}'...")
                    name_bytes = name.encode('utf-8').ljust(12, b'\x00')[:12]
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_NAME, name_bytes))
                    await asyncio.sleep(delay_between_commands)
                
                # 6. Alterar TX Power
                if tx_power is not None:
                    print(f"Alterando TX Power para {tx_power}...")
                    tx_bytes = struct.pack('b', tx_power) # 'b' = signed char
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_TX_POWER, tx_bytes))
                    await asyncio.sleep(delay_between_commands)

                # 7. Alterar Advertising Interval
                if adv_interval is not None:
                    print(f"Alterando ADV Interval (Índice {adv_interval})...")
                    adv_bytes = struct.pack('B', adv_interval) # 'B' = unsigned char
                    await client.write_gatt_char(self.UART_RX_CHAR_UUID, self._build_packet(self.CMD_ADV_INTERVAL, adv_bytes))
                    await asyncio.sleep(delay_between_commands)

                print(f"\n[{self.mac_address}]  Todas as configurações foram enviadas com sucesso!")
                return True

            except Exception as e:
                print(f"[{self.mac_address}]  Ocorreu um erro durante a escrita: {e}")
                return False
