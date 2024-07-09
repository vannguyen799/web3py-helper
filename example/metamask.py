import time
import requests
from src import Web3Helper

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}


def routes_wait_for_success(route_api, wait_seconds=10):
    wait_routes_second = wait_seconds
    _data = None

    print(f'start fetch: {route_api}')
    while wait_routes_second > 0:
        _data = requests.get(route_api, headers=headers).json()
        try:
            tx = _data[0]["trade"]
            if 'maxGas' in _data[0]:
                tx['gas'] = _data[0]['maxGas']
            return tx
        except Exception as e:
            print('error: ' + str(e))
            wait_routes_second -= 1
            time.sleep(1)
    return None


class Metamask(Web3Helper):
    def __init__(self, rpc_url, private_key):
        super().__init__(rpc_url, private_key)

    def bridge_build_tx(self, des_chain_id, src_token_address, des_token_address, src_amount, slippage=1):
        if des_chain_id == self.chain_id:
            raise ValueError('SAME CHAIN???')
        quote = (f'https://bridge.api.cx.metamask.io/getQuote'
                 f'?walletAddress={self.public_key}'
                 f'&srcChainId={self.chain_id}&destChainId={des_chain_id}'
                 f'&srcTokenAddress={src_token_address}'
                 f'&destTokenAddress={des_token_address}'
                 f'&srcTokenAmount={int(src_amount)}&slippage={slippage}'
                 f'&aggIds=lifi,socket,squid&insufficientBal=true')
        return routes_wait_for_success(quote, 30)

    def swap_build_tx(self, src_token_address, des_token_address, src_amount, slippage=5):
        quote = (f'https://swap.metaswap.codefi.network/networks/{self.chain_id}/trades'
                 f'?sourceAmount={int(src_amount)}'
                 f'&sourceToken={src_token_address}'
                 f'&destinationToken={des_token_address}'
                 f'&slippage={slippage}'
                 f'&walletAddress={self.public_key}'
                 f'&timeout=10000&enableDirectWrapping=true&includeRoute=true')
        return routes_wait_for_success(quote)

    def bridge_ETH_to_LineaETH(self, amount_eth):
        balance = self.get_balance()
        if balance < int(amount_eth * pow(10, 18)):
            raise ValueError(f"not enough ETH: got {amount_eth} ETH, available {balance}")
        linea_chain_id = '59144'
        tx = self.bridge_build_tx(linea_chain_id, self.ZERO_ADDRESS, self.ZERO_ADDRESS, amount_eth * pow(10, 18))
        if tx is None:
            raise ValueError('can not find route')
        return self.check_send_transaction(tx, 'bridge_ETH_to_LineaETH ')

    def swap_ETH(self, amount_eth, des_token_address):
        balance = self.get_balance()
        if balance < int(amount_eth * pow(10, 18)):
            raise ValueError(f"not enough ETH: got {amount_eth} ETH, available {balance}")

        tx = self.swap_build_tx(self.ZERO_ADDRESS, des_token_address, amount_eth * pow(10, 18))

        if tx is None:
            raise ValueError('can not find route')
        tx['value'] = int(amount_eth * pow(10, 18))
        return self.check_send_transaction(tx, f'swap {amount_eth} ETH to {des_token_address}')

    def swap_token(self, src_token_address, des_token_address, src_amount='all'):
        balance = self.get_token_balance(src_token_address)
        decimals = self.get_token_decimals(src_token_address)
        src_balance = 0
        if src_amount == 'all':
            src_balance = balance
        else:
            raise NotImplementedError()

        if balance < src_balance:
            raise ValueError(f"not enough ETH: got {src_amount} , available {balance}")

        tx = self.swap_build_tx(src_token_address, des_token_address, int(src_balance))
        print(tx)

        self.check_approve(src_token_address, tx['to'])
        if tx is None:
            raise ValueError('can not find route')
        return self.check_send_transaction(tx, f'swap {src_amount} to {des_token_address}')


if __name__ == '__main__':
    from src import RPC_URL

    private_key = '0xPK'

    metamask = Metamask(RPC_URL.Ethereum, private_key)
    metamask.send_mode = False
    metamask.bridge_ETH_to_LineaETH(0.1)
