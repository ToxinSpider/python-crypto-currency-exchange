from typing import Optional

from pcce.providers.kucoin.orders.order import KuCoinOrder


class KuCoinMarketOrder(KuCoinOrder):
    def __init__(
        self,
        side: str,
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
        force_hold: Optional[bool] = None
    ):
        super().__init__(
            side,
            symbol,
            "market",
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
