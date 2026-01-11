#!/usr/bin/env python3
"""
NUM-INFO
Author : azod814
Legal & Educational Phone Number Intelligence Tool
"""

import os
import json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box

console = Console()

# ---------------- CLEAR SCREEN ---------------- #
def clear():
    os.system("clear")

# ---------------- BANNER ---------------- #
def banner():
    text = Text("""
███╗   ██╗██╗   ██╗███╗   ███╗      ██╗███╗   ██╗███████╗ ██████╗ 
████╗  ██║██║   ██║████╗ ████║      ██║████╗  ██║██╔════╝██╔═══██╗
██╔██╗ ██║██║   ██║██╔████╔██║█████╗██║██╔██╗ ██║█████╗  ██║   ██║
██║╚██╗██║██║   ██║██║╚██╔╝██║╚════╝██║██║╚██╗██║██╔══╝  ██║   ██║
██║ ╚████║╚██████╔╝██║ ╚═╝ ██║      ██║██║ ╚████║██║     ╚██████╔╝
╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝      ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 

NUM-INFO | Phone Number Intelligence
Author: azod814
""", style="bold green")

    console.print(
        Panel(
            text,
            border_style="green",
            box=box.DOUBLE,
            padding=(1, 4)
        )
    )

# ---------------- LOAD PUBLIC NAMES ---------------- #
def load_public_names():
    try:
        with open("public_names.json", "r") as f:
            return json.load(f)
    except:
        return {}

# ---------------- COUNTRY LIST ---------------- #
def select_country():
    countries = [
        ("INDIA", "+91"),
        ("PAKISTAN", "+92"),
        ("UNITED STATES", "+1"),
        ("UNITED KINGDOM", "+44"),
        ("UAE", "+971"),
        ("CANADA", "+1"),
        ("AUSTRALIA", "+61"),
        ("GERMANY", "+49"),
        ("FRANCE", "+33"),
        ("NEPAL", "+977"),
        ("BANGLADESH", "+880"),
        ("SRI LANKA", "+94")
    ]

    table = Table(
        title="[bold green]Select Country[/bold green]",
        box=box.DOUBLE,
        header_style="bold green",
        padding=(0, 2)
    )
    table.add_column("No.", style="bold cyan", justify="center")
    table.add_column("Country", style="bold white")
    table.add_column("Code", style="bold yellow")

    for i, (name, code) in enumerate(countries, start=1):
        table.add_row(str(i), name, code)

    console.print(table)

    choice = Prompt.ask(
        "Select country number",
        choices=[str(i) for i in range(1, len(countries) + 1)]
    )

    idx = int(choice) - 1
    return countries[idx]

# ---------------- ANALYSIS ---------------- #
def analyze(full_number):
    try:
        parsed = phonenumbers.parse(full_number, None)
    except:
        console.print("[bold red]Invalid phone number[/bold red]")
        return None

    return {
        "country": geocoder.description_for_number(parsed, "en"),
        "country_code": f"+{parsed.country_code}",
        "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
        "timezone": ", ".join(timezone.time_zones_for_number(parsed)),
        "international": phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "national": phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "type": phonenumbers.number_type(parsed)
    }

# ---------------- RESULT ---------------- #
def show_result(data, public_name):
    table = Table(
        title="[bold green]NUM-INFO RESULT[/bold green]",
        box=box.DOUBLE,
        header_style="bold green",
        padding=(0, 2)
    )

    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="bold white")

    table.add_row("Country", data["country"])
    table.add_row("Country Code", data["country_code"])
    table.add_row("International Format", data["international"])
    table.add_row("National Format", data["national"])
    table.add_row("Current SIM / Carrier", data["carrier"])
    table.add_row("Time Zone", data["timezone"])
    table.add_row("Public Name", public_name if public_name else "-")

    console.print("\n")
    console.print(table)

    console.print(
        Panel(
            "[bold yellow]Carrier & country data is based on public telecom metadata.\n"
            "After MNP, carrier info may sometimes be outdated.[/bold yellow]",
            border_style="green",
            padding=(1, 3)
        )
    )

# ---------------- MAIN ---------------- #
def main():
    clear()
    banner()

    public_db = load_public_names()

    country_name, country_code = select_country()
    number = Prompt.ask(
        f"Enter phone number for [bold green]{country_name}[/bold green]",
        show_default=False
    )

    full_number = f"{country_code}{number}"
    data = analyze(full_number)
    if not data:
        return

    public_name = public_db.get(full_number, "")
    show_result(data, public_name)

if __name__ == "__main__":
    main()
