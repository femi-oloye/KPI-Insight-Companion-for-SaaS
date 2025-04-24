import pandas as pd

def calculate_kpis(df: pd.DataFrame) -> dict:
    kpis = {}
    
    total_leads = df["leads"].sum()
    total_customers = df["new_customers"].sum()
    total_revenue = df["revenue"].sum()
    total_ad_spend = df["ad_spend"].sum()
    
    # CAC
    kpis["CAC"] = round(total_ad_spend / total_customers, 2)
    
    # LTV (simplified)
    kpis["LTV"] = round((total_revenue / total_customers) * 3, 2)
    
    # Conversion Rate
    kpis["Conversion Rate"] = round((total_customers / total_leads) * 100, 2)
    
    # Churn (dummy, simulate ~5%)
    kpis["Churn Rate"] = round(5 + (2 * (1 - kpis["Conversion Rate"] / 100)), 2)

    return kpis
