from typing import Dict, Any


def format_bytes(
    value: int
) -> str:

    if value < 1024:
        return f"{value} B"

    if value < 1024 ** 2:
        return f"{value / 1024:.2f} KB"

    if value < 1024 ** 3:
        return f"{value / (1024 ** 2):.2f} MB"

    return f"{value / (1024 ** 3):.2f} GB"


def format_number(
    value: int
) -> str:

    return f"{value:,}"


def format_btc(
    value: float
) -> str:

    return f"{value:.8f} BTC"


def format_fee_rate(
    value: float
) -> str:

    return f"{value:.2f} sat/vB"


def format_percentage(
    value: float
) -> str:

    return f"{value:.2f}%"


def format_transaction(
    transaction: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "txid": transaction.get(
            "txid"
        ),
        "fee": transaction.get(
            "fee",
            0
        ),
        "vsize": transaction.get(
            "vsize",
            0
        ),
        "value": transaction.get(
            "value",
            0
        )
    }


def format_block(
    block: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "id": block.get(
            "id"
        ),
        "height": block.get(
            "height"
        ),
        "timestamp": block.get(
            "timestamp"
        ),
        "size": block.get(
            "size"
        ),
        "weight": block.get(
            "weight"
        ),
        "tx_count": block.get(
            "tx_count"
        ),
        "fee_range": block.get(
            "feeRange",
            []
        )
    }