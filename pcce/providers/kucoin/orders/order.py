from copy import deepcopy
from typing import Optional

from pcce.common.utils import flat_uuid
from pcce.providers.kucoin.validations.order_property_validations import (
    validate_side, validate_stop, validate_stop_loss_take_profit)


class KuCoinOrder:
    def __init__(
        self,
        side: str,
        symbol: str,
        _type: str,
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
        force_hold: Optional[bool] = None
    ):
        """General kucoin order.

        Args:
            side (str): buy or sell
            symbol (str): a valid contract code. e.g. XBTUSDM
            _type (str): Either limit or market
            leverage (str): Leverage of the order
            size (int): _description_
            client_oid (Optional[bool], optional): Unique order id created by 
                users to identify their orders, e.g. UUID, Only allows 
                numbers, characters, underline(_), and separator(-).
            remark (Optional[str], optional): Remark for the order, length 
                cannot exceed 100 utf8 characters.
            stop (Optional[str], optional): Either down or up. Requires 
                stopPrice and stopPriceType to be defined
            stop_price (Optional[str], optional): Either TP, IP or MP, Need
                to be defined if stop is specified.
            stop_price_type (Optional[str], optional): Need to be defined 
                if stop is specified.
            take_profit (Optional[str], optional): 
            stop_loss (Optional[str], optional): 
            reduce_only (Optional[str], optional): A mark to reduce the 
                position size only. Set to false by default. Need to set 
                the position size when reduceOnly is true.
            close_order (Optional[str], optional): A mark to close the 
                position. Set to false by default. It will close all 
                the positions when closeOrder is true.
            force_hold (Optional[bool], optional): A mark to forcely 
                hold the funds for an order, even though it's an order 
                to reduce the position size. This helps the order stay 
                on the order book and not get canceled when the position 
                size changes. Set to false by default.
        """
        # Validate input
        validate_side(side)
        validate_stop(stop, stop_price, stop_price_type)
        validate_stop_loss_take_profit(stop, stop_loss, take_profit)

        # Set mandatory parameters
        self.side = side
        self.symbol = symbol
        self.leverage = leverage
        self.size = size
        self._type = _type

        # Set optional paraemters
        self.client_oid = client_oid if client_oid else flat_uuid()
        self.remark = remark
        self.stop = stop
        self.stop_price = stop_price
        self.stop_price_type = stop_price_type
        self.reduce_only = reduce_only
        self.close_order = close_order
        self.force_hold = force_hold
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    @classmethod
    def from_dict(cls, params):
        return cls(**params)

    @staticmethod
    def flip_side(side: str) -> str:
        if side == "buy":
            return "sell"
        return "buy"

    def _populate_new_order(self):
        new_order = deepcopy(self)
        new_order.client_oid = flat_uuid()
        new_order.stop_price_type = "TP"
        new_order.reduce_only = True
        return new_order

    def populate_stop_loss_order(self):
        new_order = self._populate_new_order()
        new_order.side = self.flip_side(self.side)
        new_order.stop = "down"
        new_order.stop_price = self.stop_loss
        return new_order

    def populate_take_profit_order(self):
        new_order = self._populate_new_order()
        new_order.side = self.flip_side(self.side)
        new_order.stop = "up"
        new_order.stop_price = self.take_profit
        return new_order

    def populate_stop_loss_take_profit_order(self):
        return (
            self.populate_stop_loss_order(),
            self.populate_take_profit_order()
        )

    def as_dict(self):
        return {
            'side': self.side,
            'symbol': self.symbol,
            'type': self._type,
            'leverage': self.leverage,
            'size': self.size,
            'clientOid': self.client_oid,
            'remark': self.remark,
            'stop': self.stop,
            'stopPrice': self.stop_price,
            'stopPriceType': self.stop_price_type,
            'reduceOnly': self.reduce_only,
            'closeOrder': self.close_order,
            'forceHold': self.force_hold,
        }
