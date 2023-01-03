
class Asset:
    """Parent class"""

    def __init__(self, security_code):
        self.asset_code = security_code
        self.name = None
        self.price = None
        self.price_currency = None
        self.shares = None
        self.exchange = None
        self.ideal_price = None
        self.current_irr = None
        self.risk_premium = None
        self.is_updated = None
        self.periodic_payment = None  # dividend for stocks and coupon for bonds
        self.last_fy = None  # last coupon date for bonds
        self.invest_horizon = None
        self.unit_cost = None
        self.total_units = None
