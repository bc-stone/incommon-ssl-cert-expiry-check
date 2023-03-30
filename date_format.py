from datetime import datetime


def date_formatter():
    year = datetime.now().year
    month = datetime.now().month + 1

    if len(str(month)) == 1:
        month = f"0{month}"

    start_date = f"{year}-{month}-01T00:00:00.000Z"

    if month in ["04", "06", "09", "11"]:
        end_date = f"{year}-{month}-30T00:00:00.000Z"
    elif month == "02":
        end_date = f"{year}-{month}-28T00:00:00.000Z"
    else:
        end_date = f"{year}-{month}-31T00:00:00.000Z"

    return start_date, end_date
