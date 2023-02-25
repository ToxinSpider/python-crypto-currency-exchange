from typing import Optional

from pcce.providers.kucoin.orders.order import KuCoinOrder
from pcce.providers.kucoin.validations.order_property_validations import (
    validate_post_only, validate_time_in_force)


class KuCoinLimitOrder(KuCoinOrder):
    def __init__(
        self,
        side: str,
        price: str,
        symbol: str,
        leverage: str,
        size: int,
        client_oid: Optional[bool] = None,
        remark: Optional[str] = None,
        stop: Optional[str] = None,
        stop_price: Optional[str] = None,
        stop_price_type: Optional[str] = None,
        take_profit: Optional[str] = None,
        stop_loss: Optional[str] = None,
        reduce_only: Optional[str] = None,
        close_order: Optional[str] = None,
        force_hold: Optional[bool] = None,
        time_in_force: Optional[str] = None,
        post_only: Optional[str] = None,
        hidden: Optional[str] = None,
        iceberg: Optional[str] = None,
        visible_size: Optional[str] = None
    ):
        super().__init__(
            side,
            symbol,
            "limit",
            leverage,
            size,
            client_oid,
            remark,
            stop,
            stop_price,
            stop_price_type,
            take_profit,
            stop_loss,
            reduce_only,
            close_order,
            force_hold
        )
        # Validate input
        validate_time_in_force(time_in_force)
        validate_post_only(post_only, time_in_force)

        if hidden and iceberg:
            raise
        if iceberg and not visible_size:
            raise

        # Set mandatory parameters
        self.price = price

        # Set optional paraemters
        self.hidden = hidden
        self.iceberg = iceberg
        self.visible_size = visible_size

    def as_dict(self):
        _dict = super().as_dict()
        _dict['price'] = self.price
        if self.hidden:
            _dict['hidden'] = self.hidden
        if self.iceberg:
            _dict['iceberg'] = self.iceberg
        if self.visible_size:
            _dict['visibleSize'] = self.visible_size
        return _dict
