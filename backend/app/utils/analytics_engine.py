# it is the calculator/analysis brain of this application

import pandas as pd
from datetime import datetime

RESPONDED_STATUSES = ["OA", "Interview", "Offer", "Rejected"]

def applications_to_df(applications: list) -> pd.DataFrame:   # Convert a list of SQLAlchemy Application objects into a DataFrame.

    rows = [{
        "id": a.id,
        "company": a.company,
        "role": a.role,
        "source": a.source,
        "status": a.status.value if a.status else None,
        "salary": a.salary,
        "created_at": a.created_at,
    } for a in applications]
    return pd.DataFrame(rows)  # converting list of dict into dataframe(like a table)

def compute_stats(df: pd.DataFrame) -> dict:  # convert dataframe analytics into dict
    if df.empty:
        return {
            "total_applications": 0, 
            "by_status": {}, 
            "response_rate": 0,
            "interview_conversion_rate": 0,
            "offer_rate": 0,
            "top_companies": {},
            "best_source": None,
        }

    total = len(df)  #counting df rows
    by_status = df["status"].value_counts().to_dict()  # counts unique val of status in df and convert it into dict

    responded = df["status"].isin(RESPONDED_STATUSES).sum() # checks if every ststus exists inside RESPONDED_STATUSES, mark them as true or false nd at last count all the true nd return true cnt 
    response_rate = round((responded / total) * 100, 1)

    interviewed = df["status"].isin(["Interview", "Offer"]).sum() # count applications that reached Interview OR Offer.
    interview_conversion_rate = round((interviewed / total) * 100, 1) if total else 0

    offers = by_status.get("Offer", 0) # If Offer exists, return count, otherwise 0.
    offer_rate = round((offers / interviewed) * 100, 1) if interviewed else 0

    top_companies = df["company"].value_counts().head(5).to_dict()  # return top 5 companies i have applied to most often

    source_response = (
        df.groupby("source")["status"]
        .apply(lambda s: (s.isin(RESPONDED_STATUSES).sum() / len(s)) * 100)
        .sort_values(ascending=False)
    )
    best_source = source_response.index[0] if not source_response.empty else None

    return {
        "total_applications": total,
        "by_status": by_status,
        "response_rate": response_rate,
        "interview_conversion_rate": interview_conversion_rate,
        "offer_rate": offer_rate,
        "top_companies": top_companies,
        "best_source": best_source,
    }


def compute_weekly_trend(df: pd.DataFrame) -> list[dict]: # return list of dict ,where each dict represents one week
    if df.empty:
        return []
    df = df.copy()
    df["week"] = pd.to_datetime(df["created_at"]).dt.to_period("W").astype(str)
    weekly = df.groupby("week").size().reset_index(name="count")
    return weekly.to_dict(orient="records")

def compute_funnel(df: pd.DataFrame) -> dict: # counts how many applications are at each stage of hiring like saved,applied ,oa ....
    if df.empty:
        return {}
    order = ["Saved", "Applied", "OA", "Interview", "Offer"]
    counts = df["status"].value_counts() # for each staatus , gets its count
    return {status: int(counts.get(status, 0)) for status in order}