from typing import Optional


def satoshi_to_btc(satoshis: int) -> float:
    """Convert satoshis to BTC."""
    return round(satoshis / 100_000_000, 8)


def btc_to_satoshi(btc: float) -> int:
    """Convert BTC to satoshis."""
    return int(btc * 100_000_000)


def calculate_fee_rate(
    fee: int,
    vsize: int
) -> float:
    """Calculate transaction fee rate in sat/vB."""

    if not vsize or vsize <= 0:
        return 0.0

    return round(fee / vsize, 2)


def calculate_mempool_usage(
    vsize: int,
    max_vsize: int = 300_000_000
) -> float:
    """
    Estimate mempool memory usage percentage.

    The default 300 MB capacity is used as a visualization
    reference only.
    """

    if max_vsize <= 0:
        return 0.0

    percentage = (
        vsize / max_vsize
    ) * 100

    return round(
        min(percentage, 100),
        2
    )


def calculate_congestion_score(
    tx_count: int,
    vsize: int,
    max_vsize: int = 300_000_000
) -> float:
    """
    Generate a 0-100 congestion score.

    This is a project-specific visualization score,
    not an official Bitcoin network metric.
    """

    usage = calculate_mempool_usage(
        vsize,
        max_vsize
    )

    # Transaction-count component.
    tx_score = min(
        tx_count / 2000,
        100
    )

    score = (
        usage * 0.75
        + tx_score * 0.25
    )

    return round(
        min(score, 100),
        2
    )


def congestion_level(
    score: float
) -> str:
    """Convert congestion score into a readable level."""

    if score < 25:
        return "Low"

    if score < 50:
        return "Moderate"

    if score < 75:
        return "High"

    return "Critical"


def estimate_confirmation_time(
    fee_rate: float
) -> str:
    """
    Simple fee-based visualization estimate.

    This is not a guarantee of confirmation time.
    """

    if fee_rate >= 20:
        return "Next block"

    if fee_rate >= 10:
        return "1-3 blocks"

    if fee_rate >= 5:
        return "3-6 blocks"

    if fee_rate >= 2:
        return "6-12 blocks"

    return "12+ blocks"


def safe_float(
    value: Optional[float],
    default: float = 0.0
) -> float:

    try:
        return float(value)
    except (
        TypeError,
        ValueError
    ):
        return default


def safe_int(
    value,
    default: int = 0
) -> int:

    try:
        return int(value)
    except (
        TypeError,
        ValueError
    ):
        return default