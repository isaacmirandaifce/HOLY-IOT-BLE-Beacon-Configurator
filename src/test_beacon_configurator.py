import asyncio
from beacon_configurator import BeaconConfigurator

async def main():
    # 1. Cria a instância apontando para o MAC do beacon desejado
    beacon1 = BeaconConfigurator("E4:A1:80:DD:40:57")
    
    # 2. Define o que você quer alterar (o que não for passado, não será alterado)
    sucesso = await beacon1.configure(
        password_hex="aa14061112", # Envia a senha, se necessário para desbloquear
        name="tagBLE01",
        major=20000,
        minor=19000,
    )
    
    if sucesso:
        print("Beacon 1 pronto para uso!")
        
    # Exemplo configurando um SEGUNDO beacon em lote:
    # beacon2 = BeaconConfigurator("AA:BB:CC:DD:EE:FF")
    # await beacon2.configure(major=10002, minor=19401)

if __name__ == "__main__":
    asyncio.run(main())
