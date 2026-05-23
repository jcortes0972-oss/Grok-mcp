import os
import httpx
from fastmcp import FastMCP

# Initialize a clean, simple utility connector app
app = FastMCP("LiveUtilityBridge")

@app.tool()
def get_crypto_price(coin_id: str = "bitcoin") -> str:
    """Fetches the current live price and 24h change of any cryptocurrency (e.g., bitcoin, ethereum, solana)."""
    try:
        url = f"https://coingecko.com{coin_id.lower()}&vs_currencies=usd&include_24hr_change=true"
        response = httpx.get(url, timeout=10.0)
        data = response.json()
        
        if coin_id.lower() in data:
            price = data[coin_id.lower()]["usd"]
            change = data[coin_id.lower()]["usd_24h_change"]
            return f"The current price of {coin_id.capitalize()} is ${price:,.2f} USD (24h Change: {change:+.2f}%)."
        return f"Could not find cryptocurrency tracking data for '{coin_id}'."
    except Exception as e:
        return f"Error fetching cryptocurrency market rates: {str(e)}"

@app.tool()
def get_world_time(timezone: str = "America/New_York") -> str:
    """Pulls the exact current live time and date for any major global timezone identifier."""
    try:
        url = f"https://timeapi.io{timezone}"
        response = httpx.get(url, timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            return f"Current time in {timezone}: {data['time']} on {data['date']} ({data['dayOfWeek']})."
        return f"Could not find timezone data for '{timezone}'."
    except Exception as e:
        return f"Error retrieving live timezone data clock: {str(e)}"

if __name__ == "__main__":
    # Render binds automatically to this port system environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(transport="sse", host="0.0.0.0", port=port)
