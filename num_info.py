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

Legal Phone Number Information Tool
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

# ---------------- COUNTRY SELECT ---------------- #

def select_country():
    table = Table(box=box.SIMPLE, header_style="bold green")
    table.add_column("Option")
    table.add_column("Country")
    table.add_column("Code")

    table.add_row("1", "India", "+91")
    table.add_row("2", "Pakistan", "+92")
    table.add_row("3", "Manual", "Custom")

    console.print(table)
    choice = Prompt.ask("Choose option", choices=["1", "2", "3"])

    if choice == "1":
        return "India", "+91"
    elif choice == "2":
        return "Pakistan", "+92"
    else:
        return Prompt.ask("Country name"), Prompt.ask("Country code (with +)")

# ---------------- OPERATOR LOGIC ---------------- #

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
        "If SIM was ported, old operator may appear in many tools."
    )

    console.print("\n")
    console.print(table)

    console.print(
        Panel(
            "[bold yellow]Only public & user-provided data is used.\n"
            "No private databases or KYC records accessed.[/bold yellow]",
            border_style="green"
        )
    )

# ---------------- MAIN ---------------- #

def main():
    banner()
    public_db = load_public_names()
    country, code = select_country()

    number = Prompt.ask("Enter phone number (without country code)")
    if not number.isdigit():
        console.print("[bold red]Invalid number[/bold red]")
        sys.exit(1)

    public_name = public_db.get(f"{code}{number}", "")

    show_result(country, code, number, public_name)

if __name__ == "__main__":
    main()
