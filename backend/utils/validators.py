def validate_limit(
    limit: int,
    minimum: int = 1,
    maximum: int = 100
) -> int:

    if limit < minimum:
        return minimum

    if limit > maximum:
        return maximum

    return limit


def validate_transaction_id(
    txid: str
) -> bool:

    if not txid:
        return False

    return (
        len(txid) == 64
        and all(
            character in
            "0123456789abcdefABCDEF"
            for character in txid
        )
    )


def validate_block_height(
    height: int
) -> bool:

    return height > 0