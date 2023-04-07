import contextlib
import json
import os

import requests
from rich.console import Console
from rich.table import Table

from date_format import date_formatter
from get_secrets import get_secrets
from send_email import send_email

# Email info - `recipient` can be a single string or
# a bracketed list of strings
subject = "Expiring SSL Certificates"
sender = "<CHANGEME>"
recipient = ["<CHANGEME>"]
body = "Expiring SSL Certs"
filename = "expiring_certs.txt"

start_date = date_formatter()[0]
end_date = date_formatter()[1]

secrets = get_secrets(
    url=os.getenv("VAULT_URL"),
    token=os.getenv("INCOMMON_TOKEN"),
    path=os.getenv("INCOMMON_PATH"),
)

url = secrets["data"]["report_url"]
login = secrets["data"]["login"]
password = secrets["data"]["password"]
customerUri = secrets["data"]["customerUri"]

headers = {
    "Content-Type": "application/json;charset=utf-8",
    "login": login,
    "password": password,
    "customerUri": customerUri,
}

params = {
    "from": f"{start_date}",
    "to": f"{end_date}",
    "certificateDateAttribute": 3,  # Attribute 3 is the certificate expiry date
}

response = requests.post(url, headers=headers, data=json.dumps(params)).text
results = json.loads(response)

table = Table()
table.show_lines = True
table.add_column("COMMON NAME", justify="left", style="blue")
table.add_column("EXPIRES", justify="left", style="blue")
table.add_column(
    "SUBJECT ALTERNATE NAMES", justify="left", style="blue", max_width=50
)

for i in range(len(results["reports"])):
    if (
        results["reports"][i]["status"] == "Issued"
        and "subjAltNames" in results["reports"][i].keys()
    ):
        table.add_row(
            results["reports"][i]["commonName"],
            results["reports"][i]["expires"].split("T")[0],
            results["reports"][i]["subjAltNames"],
        )
    elif results["reports"][i]["status"] == "Issued":
        table.add_row(
            results["reports"][i]["commonName"],
            results["reports"][i]["expires"].split("T")[0],
        )

console = Console(record=True)
console.print(table)
console.save_text(filename)

send_email(
    subject=subject,
    sender=sender,
    recipient=recipient,
    body=body,
    filename=filename,
)


with contextlib.suppress(FileNotFoundError):
    os.remove(filename)
