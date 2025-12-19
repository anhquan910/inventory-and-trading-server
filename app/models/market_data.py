from sqlalchemy import Column, Integer, Float, Date, BigInteger
from app.db.base_class import Base

class MarketData(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)

    # --- Target: Gold Price (The first few columns in CSV) ---
    gold_open = Column(Float)
    gold_high = Column(Float)
    gold_low = Column(Float)
    gold_close = Column(Float)
    gold_adj_close = Column(Float)
    gold_volume = Column(BigInteger)

    # --- S&P 500 (SP) ---
    sp_open = Column(Float)
    sp_high = Column(Float)
    sp_low = Column(Float)
    sp_close = Column(Float)
    sp_adj_close = Column(Float)
    sp_volume = Column(BigInteger)

    # --- Dow Jones (DJ) ---
    dj_open = Column(Float)
    dj_high = Column(Float)
    dj_low = Column(Float)
    dj_close = Column(Float)
    dj_adj_close = Column(Float)
    dj_volume = Column(BigInteger)

    # --- ETF Gold / Other Asset (EG) ---
    eg_open = Column(Float)
    eg_high = Column(Float)
    eg_low = Column(Float)
    eg_close = Column(Float)
    eg_adj_close = Column(Float)
    eg_volume = Column(BigInteger)

    # --- EUR/USD (EU) ---
    eu_price = Column(Float)
    eu_open = Column(Float)
    eu_high = Column(Float)
    eu_low = Column(Float)
    eu_trend = Column(Integer) # Assuming Trend is 1/0 or categorical code

    # --- Brent Oil? (OF) ---
    of_price = Column(Float)
    of_open = Column(Float)
    of_high = Column(Float)
    of_low = Column(Float)
    of_volume = Column(BigInteger)
    of_trend = Column(Integer)

    # --- WTI Oil? (OS) ---
    os_price = Column(Float)
    os_open = Column(Float)
    os_high = Column(Float)
    os_low = Column(Float)
    os_trend = Column(Integer)

    # --- Swiss Franc? (SF) ---
    sf_price = Column(Float)
    sf_open = Column(Float)
    sf_high = Column(Float)
    sf_low = Column(Float)
    sf_volume = Column(BigInteger)
    sf_trend = Column(Integer)

    # --- US Bonds (USB) ---
    usb_price = Column(Float)
    usb_open = Column(Float)
    usb_high = Column(Float)
    usb_low = Column(Float)
    usb_trend = Column(Integer)

    # --- Platinum (PLT) ---
    plt_price = Column(Float)
    plt_open = Column(Float)
    plt_high = Column(Float)
    plt_low = Column(Float)
    plt_trend = Column(Integer)

    # --- Palladium (PLD) ---
    pld_price = Column(Float)
    pld_open = Column(Float)
    pld_high = Column(Float)
    pld_low = Column(Float)
    pld_trend = Column(Integer)

    # --- Rhodium (RHO) ---
    rho_price = Column(Float)

    # --- US Dollar Index (USDI) ---
    usdi_price = Column(Float)
    usdi_open = Column(Float)
    usdi_high = Column(Float)
    usdi_low = Column(Float)
    usdi_volume = Column(BigInteger)
    usdi_trend = Column(Integer)

    # --- Gold Miners ETF (GDX) ---
    gdx_open = Column(Float)
    gdx_high = Column(Float)
    gdx_low = Column(Float)
    gdx_close = Column(Float)
    gdx_adj_close = Column(Float)
    gdx_volume = Column(BigInteger)

    # --- US Oil Fund (USO) ---
    uso_open = Column(Float)
    uso_high = Column(Float)
    uso_low = Column(Float)
    uso_close = Column(Float)
    uso_adj_close = Column(Float)
    uso_volume = Column(BigInteger)