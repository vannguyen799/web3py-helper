from ._web3helper import _Web3Helper
from .amounttype import AMOUNT_TYPE


class Web3Helper(_Web3Helper):
    def __init__(self, rpc_url=None, private_key=None):
        super().__init__(rpc_url=rpc_url, private_key=private_key)
        self._send_eth_gas = None

    def check_send_transaction(self, tx: dict, title: str = ' ') -> bool:
        result = self.send_transaction(tx)
        if result == 'pass' or result.status == 1:
            print(f'[SUCCESS] {title}')
            return True
        if result.status is not None:
            print(f"[FAIL] {title}")
            return False

    def auto_amount(self):
        raise NotImplementedError()

    def amount_factory(self, token_address, amount, check_balance=True):
        balance = self.get_token_balance(token_address)
        _amount = 0
        if amount == AMOUNT_TYPE.ALL:
            _amount = balance
        elif amount == AMOUNT_TYPE.AUTO:
            _amount = self.auto_amount()
        elif amount == AMOUNT_TYPE.HALF:
            _amount = int(balance / 2)
        elif type(amount) is AMOUNT_TYPE.FIXED_DECIMALS:
            _amount = amount
        elif type(amount) is AMOUNT_TYPE.NONFIXED_DECIMALS or isinstance(amount, (int, float)):
            _amount = int(amount * pow(10, self.get_token_decimals(token_address)))

        if (_amount <= 0 or _amount > balance) and check_balance:
            raise ValueError(
                f'not enough balance for {token_address}: got {amount} current balance: {self.unparse_token_unit(self.ZERO_ADDRESS, balance)}')

        return _amount

    @property
    def send_eth_gas(self):
        if self._send_eth_gas is None:
            self._send_eth_gas = self.prepare_transaction({
                'from': self.public_key,
                'to': self.public_key,
                'value': 0
            }).get('gas')
        return self._send_eth_gas

    def set_rpc_url(self, rpc_url: str):
        self._send_eth_gas = None
        super().set_rpc_url(rpc_url)
        return self

    def get_balance_fixed(self, token_address=None):
        if token_address is None:
            token_address = self.ZERO_ADDRESS
        return self.get_balance(__token_address=token_address, remove_decimals=True)

    def mint_token(self, token_address, data, mint_fee=0, mint_contract_address=None, check_minted=True):
        mint_contract = token_address
        if mint_contract_address is not None:
            mint_contract = mint_contract_address

        if check_minted and self.get_token_balance(token_address) > 0:
            print(f'minted {token_address}')
            return True

        # mint

        return self.check_send_transaction({
            'to': mint_contract,
            'value': mint_fee,
            'data': data
        }, f'Mint {token_address}')

    def send_eth(self, send_to_address, amount_eth):
        value = self.amount_factory(self.ZERO_ADDRESS, amount_eth)
        gas = self.send_eth_gas  # gasused
        gas_price = self.gas_price
        tx = {
            'value': value - int(gas * gas_price),
            'to': send_to_address,
            'gas': gas,
            'gasPrice': gas_price
        }

        return self.check_send_transaction(tx, f'Send {amount_eth} ETH from {self.public_key} to {send_to_address}:')

