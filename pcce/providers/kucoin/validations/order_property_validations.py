from typing import Optional

from pcce.providers.kucoin.exceptions import OrderPropertyValidationException

VALID_SIDE = ("buy", "sell")
VALID_STOP = ("down", "up")
VALID_STOP_PRICE_TYPE = ("TP", "MP", "IP")
VALID_TIME_IN_FORCE = ("GTC", "IOC")


def validate_side(side: str) -> None:
    if side not in VALID_SIDE:
        raise OrderPropertyValidationException(
            f"Order 'side' need to be one of {VALID_SIDE}"
        )


def validate_stop(
    stop: Optional[str],
    stop_price: Optional[str],
    stop_price_type: Optional[str]
) -> None:
    if not stop:
        return

    if stop not in VALID_STOP:
        raise OrderPropertyValidationException(
            f"Property 'stop' need to be one of {VALID_STOP}"
        )
    if stop_price_type not in VALID_STOP_PRICE_TYPE:
        raise OrderPropertyValidationException(
            "Property 'stop_price_type' need to be "
            f"one of {VALID_STOP_PRICE_TYPE}"
        )
    if not stop_price:
        raise OrderPropertyValidationException(
            f"Property 'stop_price' need to be defined"
        )


def validate_stop_loss_take_profit(
    stop: Optional[str],
    stop_loss: Optional[str],
    take_profit: Optional[str]
) -> None:
    if stop and (stop_loss or take_profit):
        raise OrderPropertyValidationException(
            f"If property 'stop_loss' or 'take_profit' defined "
            "proerty 'stop' need to be empty"
        )


def validate_time_in_force(time_in_force: Optional[str]) -> None:
    if not time_in_force:
        return

    if time_in_force not in VALID_TIME_IN_FORCE:
        raise OrderPropertyValidationException(
            "Property 'time_in_force' need to be "
            f"one of: {VALID_TIME_IN_FORCE}"
        )


def validate_post_only(time_in_force: Optional[str], post_only: Optional[bool]) -> bool:
    if post_only and time_in_force != VALID_TIME_IN_FORCE[0]:
        raise OrderPropertyValidationException(
            "If property 'post_only' defined, "
            f"'time_in_force' need to be {VALID_TIME_IN_FORCE[0]}"
        )


def validate_hidden_and_iceberg(hidden: Optional[bool], iceberg: Optional[bool]) -> bool:
    if hidden and iceberg:
        raise OrderPropertyValidationException(
            f"Only one of 'hodden' and 'iceberg' can be defined"
        )


def validate_iceberg(iceberg: Optional[bool], visible_size: Optional[int]) -> bool:
    if iceberg and not visible_size:
        raise OrderPropertyValidationException(
            f"If property 'iceberg' is defined, proerty 'visible_size' need to be empty"
        )
