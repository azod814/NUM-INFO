#!/usr/bin/env python3
"""
NUM-INFO
Author : azod08
Purpose: Legal & Educational Phone Number OSINT Tool
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
import json
import sys
import pycountry

console = Console()

# ---------------- BANNER ---------------- #

def banner():
    banner_text = Text("""
███╗   ██╗██╗   ██╗███╗   ███╗      ██╗███╗   ██╗███████╗ ██████╗ 
████╗  ██║██║   ██║████╗ ████║      ██║████╗  ██║██╔════╝██╔═══██╗
██╔██╗ ██║██║   ██║██╔████╔██║█████╗██║██╔██╗ ██║█████╗  ██║   ██║
██║╚██╗██║██║   ██║██║╚██╔╝██║╚════╝██║██║╚██╗██║██╔══╝  ██║   ██║
██║ ╚████║╚██████╔╝██║ ╚═╝ ██║      ██║██║ ╚████║██║     ╚██████╔╝
╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝      ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 

NUM-INFO  |  Legal Phone Information Tool
Author: azod814
""", style="bold green")

    console.print(Panel(banner_text, box=box.DOUBLE, border_style="green"))

# ---------------- LOAD PUBLIC NAMES ---------------- #

def load_public_names():
    try:
        with open("public_names.json", "r") as f:
            return json.load(f)
    except:
        return {}

# ---------------- COUNTRY INPUT (UPDATED) ---------------- #

def country_input():
    console.print("\n[bold green]Country Selection[/bold green]")
    console.print(
        "[cyan]1)[/cyan] Enter country code manually (recommended)\n"
        "[cyan]2)[/cyan] Select country name (helper mode)\n"
    )

    choice = Prompt.ask("Choose option", choices=["1", "2"], default="1")

    # ---- MANUAL MODE ----
    if choice == "1":
        code = Prompt.ask("Enter country code (with +, e.g. +91)")
        return "User Selected", code

    # ---- COUNTRY LIST MODE ----
    countries = sorted(pycountry.countries, key=lambda c: c.name)

    table = Table(title="Available Countries (Reference)", box=box.SIMPLE)
    table.add_column("Country", style="green")

    for c in countries[:40]:
        table.add_row(c.name)

    console.print(table)
    console.print("[yellow]Tip:[/yellow] Type country name manually if not visible.")

    cname = Prompt.ask("Enter country name")
    return cname, "+?"

# ---------------- OPERATOR LOGIC (INDIA BASED) ---------------- #

def detect_operator(number):
    prefixes = {
        "98": "Airtel",
        "99": "Airtel",
        "97": "Jio",
        "88": "Jio",
        "90": "Vodafone/Idea",
        "94": "BSNL"
    }
    for p in prefixes:
        if number.startswith(p):
            return prefixes[p]
    return "Unknown"

# ---------------- RESULT ---------------- #

def show_result(country, code, number, public_name):
    table = Table(
        title="[bold green]NUM-INFO RESULT[/bold green]",
        box=box.DOUBLE,
        header_style="bold green"
    )

    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="bold white")

    table.add_row("Country", country)
    table.add_row("Country Code", code)
    table.add_row("Phone Number", number)
    table.add_row("Public Name", public_name if public_name else "-")
    table.add_row("Original Operator", detect_operator(number))
    table.add_row(
        "Current Operator",
        "May differ due to Mobile Number Portability (MNP)"
    )
    table.add_row(
        "Note",
        "Ported numbers often show old operator in public tools."
    )

    console.print("\n")
    console.print(table)

    console.print(
        Panel(
            "[bold yellow]This tool uses only public or user-provided data.\n"
            "No private or telecom databases are accessed.[/bold yellow]",
            border_style="green"
        )
    )

# ---------------- MAIN ---------------- #

def main():
    banner()
    public_db = load_public_names()

    country, code = country_input()

    number = Prompt.ask("Enter phone number (without country code)")
    if not number.isdigit():
        console.print("[bold red]Invalid phone number[/bold red]")
        sys.exit(1)

    full_number = f"{code}{number}"
    public_name = public_db.get(full_number, "")

    show_result(country, code, number, public_name)

if __name__ == "__main__":
    main()
