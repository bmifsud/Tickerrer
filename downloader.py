import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Optional

DATA_FILE = "stored_data.json"

def save_data(data: List[Dict[str, Any]], filepath: str = DATA_FILE) -> str:
    """Save ticker or financial data to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return filepath

def get_data(filepath: str = DATA_FILE) -> List[Dict[str, Any]]:
    """Retrieve saved data from JSON file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def generate_chart(data: Optional[List[Dict[str, Any]]] = None, output_file: str = "chart.png", filepath: str = DATA_FILE) -> str:
    """Generate and save a matplotlib line chart from ticker data."""
    if data is None:
        data = get_data(filepath)

    if not data or not data[0]:
        # Create an empty or placeholder chart if no data is available
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No Data Available", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title("Ticker Data Chart")
        fig.savefig(output_file)
        plt.close(fig)
        return output_file

    # Assuming data is a list of dicts with 'date'/'time'/'x' and 'price'/'value'/'y' or similar
    # Try common keys
    x_keys = ['date', 'time', 'timestamp', 'x']
    y_keys = ['price', 'val', 'value', 'close', 'y']

    x_key = next((k for k in x_keys if k in data[0]), list(data[0].keys())[0])
    y_key = next((k for k in y_keys if k in data[0]), list(data[0].keys())[1] if len(data[0].keys()) > 1 else list(data[0].keys())[0])

    x_vals = [item.get(x_key) for item in data]
    y_vals = [item.get(y_key) for item in data]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label=y_key.capitalize())
    ax.set_xlabel(x_key.capitalize())
    ax.set_ylabel(y_key.capitalize())
    ax.set_title(f"Ticker Chart ({y_key.capitalize()} over {x_key.capitalize()})")
    ax.tick_params(axis='x', labelrotation=45)
    fig.tight_layout()
    ax.legend()
    fig.savefig(output_file)
    plt.close(fig)

    return output_file
