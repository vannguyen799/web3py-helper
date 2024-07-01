class AMOUNT_TYPE:
    ALL = 'all'
    AUTO = 'auto'
    HALF = 'half'

    class FIXED_DECIMALS(int):
        def __new__(cls, value: int):
            return super().__new__(cls, int(value))

    class NONFIXED_DECIMALS(float):
        def __new__(cls, value: float | int):
            return super().__new__(cls, value)


