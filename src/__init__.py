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


EthereumWeb3 = Web3Helper(RPC_URL.Ethereum)
PolygonWeb3 = Web3Helper(RPC_URL.Polygon)  # MATIC
BinanceWeb3 = Web3Helper(RPC_URL.Binance)  # BNB
LineaWeb3 = Web3Helper(RPC_URL.Linea)  # ETH
ArbitrumWeb3 = Web3Helper(RPC_URL.Arbitrum)  #
ZKSyncEraWeb3 = Web3Helper(RPC_URL.ZKSyncEra)  # ETH
OptimismWeb3 = Web3Helper(RPC_URL.Optimism)  #
ScrollWeb3 = Web3Helper(RPC_URL.Scroll)  # ETH
MantleWeb3 = Web3Helper(RPC_URL.Mantle)  # MTL
ZKFairWeb3 = Web3Helper(RPC_URL.ZKFair)  # USDC
KucoinWeb3 = Web3Helper(RPC_URL.Kucoin)  # KCS
MantaWeb3 = Web3Helper(RPC_URL.Manta)
