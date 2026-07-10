from account.instrument_cache import InstrumentCache


def get_tick_size(symbol: str) ->float:

    instrument = InstrumentCache.get(symbol)

    if instrument is None:
        raise ValueError(f"{symbol} not found in instrument cache")

    return float(instrument["tick_size"])
