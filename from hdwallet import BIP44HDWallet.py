from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
import pandas as pd
import time

# Получить от пользователя количество кошельков для создания
num_wallets = int(input("Введите количество кошельков для создания: "))

if num_wallets <= 0:
    raise ValueError("Пожалуйста, введите положительное целое число.")

# Установка BIP44-пути для Ethereum
bip44_derivation_path = "m/0"
bip44_derivation = BIP44Derivation(cryptocurrency=EthereumMainnet, account=0, change=False, address=0)

# Инициализация Ethereum BIP44HDWallet
bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)

# Создание списка словарей для хранения информации о кошельках
wallet_info_list = []

# Цикл по количеству кошельков для создания
for i in range(num_wallets):
    # Генерирование случайной 12-словной мнемонической фразы
    mnemonic = generate_mnemonic()
    # Получение производного адреса Ethereum BIP44HDWallet
    bip44_hdwallet.from_mnemonic(mnemonic=mnemonic)
    bip44_hdwallet.from_path(path=bip44_derivation_path)

    # Получение приватного ключа и адреса
    private_key = bip44_hdwallet.private_key()
    address = bip44_hdwallet.address()

    # Сохранение информации о кошельке в словаре
    wallet_info = {
        "mnemonic_phrase": mnemonic,
        "private_key": private_key,
        "address": address,
    }

    # Добавление информации о кошельке в список
    wallet_info_list.append(wallet_info)

# Создание таблицы из списка словарей
df = pd.DataFrame(wallet_info_list)

# Запись таблицы в файл Excel
df.to_excel("wallet_info.xlsx", index=False)

print(f"Успешно создано {num_wallets} кошельков и сохранена информация в файле wallet_info.xlsx.")
