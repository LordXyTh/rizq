def calculate_weighted_market_cap(market_cap, total_market_cap):
    return round(float(market_cap) / total_market_cap * 100, 2) if total_market_cap else 0
