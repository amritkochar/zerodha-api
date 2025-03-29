# kite_client/client.py

import requests
from . import auth, config
from tabulate import tabulate  # at the top of the file
from . import cache
import datetime  # at the top of client.py



class KiteClient:
    def __init__(self):
        self.api_key = config.API_KEY
        self.access_token = auth.authenticate()

    def _headers(self):
        return {
            "X-Kite-Version": "3",
            "Authorization": f"token {self.api_key}:{self.access_token}"
        }
    
    def _request(self, method, url, **kwargs):
        headers = self._headers()
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            if response.status_code == 403:
                print("⚠️ Access token expired. Re-authenticating...")
                self.access_token = auth.authenticate(force_refresh=True)
                headers = self._headers()
                response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("❌ API request failed:", e)
            raise


    def get_profile(self):
        url = "https://api.kite.trade/user/profile"
        return requests.get(url, headers=self._headers()).json()

    def get_holdings(self):
        """Return cached holdings or fetch fresh if expired."""
        data, timestamp = cache.load_cache("holdings", ttl_seconds=3600)
        if data:
            return {"data": data, "cached_at": timestamp}

        response = self._request("GET", "https://api.kite.trade/portfolio/holdings")
        if "data" in response:
            cache.save_cache("holdings", response["data"])
            response["cached_at"] = time.time()
        return response

    def print_holdings(self, sort_by="tradingsymbol"):
        """
        Fetch and print holdings in a readable table format.
        """
        holdings = self.get_holdings()
        if "data" not in holdings:
            print("⚠️ Failed to fetch holdings.")
            return

        data = holdings["data"]

        if sort_by:
            data = sorted(data, key=lambda x: x.get(sort_by, ""))

        table = []
        for h in data:
            table.append([
                h.get("tradingsymbol"),
                h.get("quantity"),
                h.get("average_price"),
                h.get("last_price"),
                h.get("pnl")
            ])

        headers = ["Symbol", "Qty", "Avg Price", "LTP", "PnL"]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        ts = holdings.get("cached_at")
        if ts:
            dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n📅 Last updated at: {dt}")

    def get_mf_holdings(self):
        data, timestamp = cache.load_cache("mf_holdings", ttl_seconds=3600)
        if data:
            return {"data": data, "cached_at": timestamp}

        response = self._request("GET", "https://api.kite.trade/mf/holdings")
        if "data" in response:
            cache.save_cache("mf_holdings", response["data"])
            response["cached_at"] = time.time()
        return response
 
    def print_mf_holdings(self, sort_by="fund"):
        """Print mutual fund holdings in a clean table format."""
        holdings = self.get_mf_holdings()
        if "data" not in holdings:
            print("⚠️ No mutual fund holdings data found.")
            return

        data = holdings["data"]

        if not data:
            print("📭 No mutual fund holdings available.")
            return

        if sort_by:
            data = sorted(data, key=lambda x: x.get(sort_by, ""))

        table = []
        for h in data:
            table.append([
                h.get("fund"),             # Fund name
                h.get("folio"),            # Folio ID
                h.get("quantity"),         # Units
                h.get("average_price"),    # Purchase NAV
                h.get("last_price"),       # Current NAV
                h.get("pnl"),              # Profit/Loss
                h.get("tradingsymbol")     # Symbol code
            ])

        headers = ["Fund", "Folio", "Units", "Buy NAV", "Current NAV", "PnL", "Symbol"]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        ts = holdings.get("cached_at")
        if ts:
            dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n📅 Last updated at: {dt}")

    def get_quote(self, instruments):
        """Get full quote for one or more instruments."""
        if isinstance(instruments, list):
            instruments = ",".join(instruments)
            print("instruments: " + instruments);
        url = f"https://api.kite.trade/quote?i={instruments}"
        return self._request("GET", url)

    def place_order(self, order_type, exchange, tradingsymbol, transaction_type,
                    quantity, product, order_class="regular", price=None, trigger_price=None):
        """Place a regular or SL order."""
        url = f"https://api.kite.trade/orders/{order_class}"
        payload = {
            "tradingsymbol": tradingsymbol,
            "exchange": exchange,
            "transaction_type": transaction_type,
            "order_type": order_type,
            "quantity": quantity,
            "product": product,
            "validity": "DAY"
        }
        if price:
            payload["price"] = price
        if trigger_price:
            payload["trigger_price"] = trigger_price

        return self._request("POST", url, data=payload)
    
    def cancel_order(self, order_id, order_class="regular"):
        """Cancel an existing order by ID."""
        url = f"https://api.kite.trade/orders/{order_class}/{order_id}"
        return self._request("DELETE", url)

    def get_positions(self):
        """Get current day's positions."""
        url = "https://api.kite.trade/portfolio/positions"
        return self._request("GET", url)

