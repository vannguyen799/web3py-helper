import math
import time

from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.contract import Contract
from eth_account.signers.local import LocalAccount


class IWeb3Helper:
    def __init__(self):
        pass


class _Web3Helper(IWeb3Helper):
    ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
    ERC20_MIN_ABI = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]'

    def __init__(self, rpc_url: str | None = None, private_key=None):
        super().__init__()
        self._private_key = None
        self._rpc_url = None
        self.web3: Web3 | None = None
        self._public_key = None

        self.set_rpc_url(rpc_url).set_private_key(private_key)
        self._increase_fee = 1.05  # increase fee gas rate
        self.gas_price_limit = 20
        self.send_mode = True  # false for only check tx
        self.wait_for_tx_receipt = True

    def set_rpc_url(self, rpc_url: str) -> "_Web3Helper":
        if rpc_url.startswith('https://'):
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        elif rpc_url.startswith('wss://') or rpc_url.startswith('ws://'):
            self.web3 = Web3(Web3.WebsocketProvider(rpc_url))
        elif rpc_url is None:
            return self
        else:
            raise ValueError(f'rpc not valid: got {rpc_url}')
        self._rpc_url = rpc_url
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return self

    @property
    def chain_id(self):
        return self.web3.eth.chain_id

    def get_signer(self) -> LocalAccount:
        return self.web3.eth.account.from_key(self._private_key)

    @property
    def gas_price(self):
        return self.web3.eth.gas_price

    @property
    def public_key(self):
        if self._public_key is None:
            self._public_key = self.to_checksum_address(self.web3.eth.account.from_key(self._private_key).address)
        return self._public_key

    def set_private_key(self, private_key) -> "_Web3Helper":
        self._public_key = None
        self._private_key = private_key
        return self

    def get_balance(self, remove_decimals=False, __token_address=None):
        if __token_address is not None:
            return self.get_token_balance(__token_address, remove_decimals)
        if remove_decimals:
            return self.web3.eth.get_balance(self.public_key) / pow(10, 18)
        return self.web3.eth.get_balance(self.public_key)

    def set_max_gas_price(self, max_price: float | None = None) -> "_Web3Helper":
        self.gas_price_limit = max_price
        return self

    def set_increase_gas_fee(self, multiply_value: float = 1) -> "_Web3Helper":
        self._increase_fee = multiply_value
        return self

    def send_transaction(self, transaction):
        _web3 = self.web3
        transaction = self.prepare_transaction(transaction)

        tx_gas_price = transaction['gasPrice'] / self.web3.to_wei(1, 'gwei')

        if self.gas_price_limit is not None:
            if float(tx_gas_price) > self.gas_price_limit:
                raise ValueError(f'Over gas price limit = {self.gas_price_limit}: Tx gas price = {tx_gas_price} ')

        print(f'sending transaction from {self.get_public_key()} :\nInput data : {transaction}')

        if self.send_mode is False:
            print(f'tx not send: {transaction}')
            return True

        signed_tx = _web3.eth.account.sign_transaction(transaction, self._private_key)
        send_tx = _web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'txhash: {_web3.to_hex(send_tx)}')
        if self.wait_for_tx_receipt is False:
            return 'pass'
        rs = _web3.eth.wait_for_transaction_receipt(_web3.to_hex(send_tx))
        while rs.status is None:
            rs = _web3.eth.wait_for_transaction_receipt(_web3.to_hex(send_tx))
            time.sleep(1)
        if rs.status == 1:
            print("DONE")
        else:
            if rs.status is not None:
                print("ERROR")
        return rs

    def get_token_contract(self, token_address, token_abi=ERC20_MIN_ABI):
        return self.get_contract(token_address, token_abi)

    def to_checksum_address(self, address):
        if address == self.ZERO_ADDRESS:
            return address
        return self.web3.to_checksum_address(address)

    def check_approve(self, token_address: str, approve_to: str, amount: float | None = None) -> bool:
        """

        :param token_address: token to approve
        :param approve_to: address will be able to spend your token
        :param amount: amount approve | default is the biggest value
        :return:
        """
        if token_address == self.ZERO_ADDRESS:
            return True
        _web3 = self.web3
        token_address = _web3.to_checksum_address(token_address)
        approve_to = _web3.to_checksum_address(approve_to)

        token_contract = self.get_token_contract(token_address)
        allowance = token_contract.functions.allowance(self.public_key, approve_to).call()
        if amount is None:
            amount = 105792089237316195423570985008687907853269984665640564039457584007913129
        else:
            amount = amount * pow(10, token_contract.functions.decimals().call())

        if int(allowance) < amount:
            print(f"APPROVING ... {token_address} to {approve_to}")
            tx = token_contract.functions.approve(approve_to,
                                                  115792089237316195423570985008687907853269984665640564039457584007913129).build_transaction(
                {
                    'from': self.get_public_key(),
                    "gasPrice": _web3.eth.gas_price,
                    "value": 0
                })
            result = self.send_transaction(tx)
            if result.status == 1:
                print('Approved')
                return True
            else:
                print('Not Approved')
                return False
        if int(allowance) > 0:
            print('Approved')
            return True
        print('Not Approved')
        return False

    def send_token_build_tx(self, receive_address, token_address, fixed_decimals_amount=None,
                            nonfixed_decimals_amount=None, token_abi=ERC20_MIN_ABI):
        token_contract = self.get_token_contract(token_address=token_address, token_abi=token_abi)
        wad = 0
        if fixed_decimals_amount is None and nonfixed_decimals_amount is not None:
            wad = self.parse_token_unit(token_address, nonfixed_decimals_amount)
        elif fixed_decimals_amount is not None and nonfixed_decimals_amount is None:
            wad = fixed_decimals_amount
        else:
            raise ValueError('missing or have two input amount')
        tx = token_contract.functions.transfer(receive_address, wad).build_transaction({
            'from': self.public_key,
            'value': 0,
            'gasPrice': math.floor(self.gas_price * self._increase_fee)
        })

        return tx

    def get_contract(self, contract_address, contract_abi) -> Contract:
        contract_address = self.to_checksum_address(contract_address)
        contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        return contract

    def get_token_balance(self, token_address, remove_decimals=False):
        balance = None
        if token_address == self.ZERO_ADDRESS:
            balance = self.get_balance()
        else:
            token_contract = self.get_contract(token_address, self.ERC20_MIN_ABI)
            balance = token_contract.functions.balanceOf(self.public_key).call()

        if remove_decimals:
            balance = balance / pow(10, self.get_token_decimals(token_address))

        return balance

    def parse_token_unit(self, token_address, amount):
        return int(amount * pow(10, self.get_token_decimals(token_address)))

    def unparse_token_unit(self, token_address, fixed_decimals_amount):
        return float(fixed_decimals_amount / pow(10, self.get_token_decimals(token_address)))

    def get_token_decimals(self, token_address) -> int:
        if token_address == self.ZERO_ADDRESS:
            return 18
        token_contract = self.get_contract(token_address, self.ERC20_MIN_ABI)
        return token_contract.functions.decimals().call()

    def prepare_transaction(self, transaction) -> dict:
        _tx = transaction
        _web3 = self.web3
        if 'from' not in _tx:
            _tx.update({'from': self.public_key})
        _tx['from'] = self.to_checksum_address(_tx['from'])
        _tx['to'] = self.to_checksum_address(_tx['to'])

        nonce = _web3.eth.get_transaction_count(_tx['from'])
        _tx.update({'nonce': nonce})

        if 'value' not in _tx:
            _tx.update({'value': _web3.to_wei(0, 'ether')})
        if str(_tx['value']).startswith('0x'):
            _tx.update({'value': int(_tx['value'], 0)})
        if type(_tx['value']) is str:
            _tx['value'] = int(_tx['value'])
        if 'chainId' not in _tx:
            _tx.update({'chainId': self.chain_id})
        if 'gasLimit' in _tx:
            _tx.update({'gas': _tx['gasLimit']})
            del _tx['gasLimit']
        if 'gas' not in _tx:
            estimate = _web3.eth.estimate_gas(_tx)
            _tx.update({'gas': int(estimate)})
        if 'gasPrice' not in _tx:
            _tx.update({'gasPrice': math.floor(self.gas_price * self._increase_fee)})
        return _tx
