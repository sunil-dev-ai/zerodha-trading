from rich.console import Console
from rich.table import Table
import webbrowser


def show_profile(profile: dict):
    console = Console()
    table = Table(title="Zerodha Profile", style="bold green")

    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    for key, value in profile.items():
        if isinstance(value, list):
            value = ", ".join(value)
        elif isinstance(value, dict):
            value = ", ".join([f"{k}:{v}" for k, v in value.items()])
        table.add_row(key, str(value))

    console.print(table)

    # # Open avatar image in browser
    # if "avatar_url" in profile:
    #     print("\n🖼 Opening avatar image in browser...")
    #     webbrowser.open(profile["avatar_url"])


if __name__ == "__main__":
    show_profile()
