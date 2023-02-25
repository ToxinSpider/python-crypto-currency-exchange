from pcce.providers.kucoin.orders import KuCoinLimitOrder


def test_limit_order_creation():
    new_order = KuCoinLimitOrder(
        side="buy",
        price="0.1",
        symbol="ETHUSDT",
        leverage="1",
        size=1
    )
    assert new_order.side == "buy"
    assert new_order.price == "0.1"
    assert new_order.symbol == "ETHUSDT"
    assert new_order.leverage == "1"
    assert new_order.size == 1

    stop_loss_order = new_order.populate_stop_loss_order()
    assert stop_loss_order.side == "sell"
    assert stop_loss_order.price == "0.1"
    assert stop_loss_order.symbol == "ETHUSDT"
    assert stop_loss_order.leverage == "1"
    assert stop_loss_order.size == 1
    
    take_profit_order = new_order.populate_take_profit_order()
    assert take_profit_order.side == "sell"
    assert take_profit_order.price == "0.1"
    assert take_profit_order.symbol == "ETHUSDT"
    assert take_profit_order.leverage == "1"
    assert take_profit_order.size == 1
