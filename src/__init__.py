from .web3helper import Web3Helper
from .amounttype import AMOUNT_TYPE


class RPC_URL:
    INFURA_API_KEY = 'INFURA_API_KEY'
    EthereumINFURA = f'https://mainnet.infura.io/v3/{INFURA_API_KEY}'
    Ethereum = 'https://eth.llamarpc.com'
    Polygon = "https://polygon.llamarpc.com"
    Binance = "https://binance.llamarpc.com"
    Linea = "https://rpc.linea.build"
    LineaBlockpi = "https://linea.blockpi.network/v1/rpc/public"
    Arbitrum = "https://arb1.arbitrum.io/rpc"
    ZKSyncEra = "https://mainnet.era.zksync.io"
    Optimism = "https://optimism.llamarpc.com"
    Scroll = "https://rpc.scroll.io"
    Mantle = "https://rpc.mantle.xyz"
    ZKFair = "https://rpc.zkfair.io"
    Kucoin = "https://rpc-mainnet.kcc.network"
    Manta = 'https://pacific-rpc.manta.network/http'
