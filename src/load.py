import pandas as pd
from sqlalchemy import create_engine

def load(df: pd.DataFrame, conn_string: str, table: str = "weather_data") -> None:
    print(f"[Load] Connecting to database...")
    engine = create_engine(conn_string)
    
    df.to_sql(
        name=table,
        con=engine,
        if_exists='append',
        index=False
    )
    print(f"[Load] Weather record written to '{table}'")