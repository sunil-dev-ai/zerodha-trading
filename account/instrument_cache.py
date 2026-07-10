from core.place_order import kite


class InstrumentCache:
    """
    Loads Zerodha instruments once and caches them.

    Lookup Time:
        O(1)
    """

    _loaded = False
    _instrument_map = {}

    @classmethod
    def load(cls, exchange="NSE"):
        if cls._loaded:
            return

        print("Loading instrument master...")

        instruments = kite.instruments(exchange)

        cls._instrument_map = {
            instrument["tradingsymbol"]: instrument
            for instrument in instruments
        }

        cls._loaded = True

        print(f"Loaded {len(cls._instrument_map)} instruments.")

    @classmethod
    def get(cls, symbol):

        if not cls._loaded:
            cls.load()

        return cls._instrument_map.get(symbol)
