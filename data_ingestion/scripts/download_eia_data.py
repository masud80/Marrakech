import os
import requests
import pandas as pd
from dotenv import load_dotenv
import shutil

# Find project root (assume this script is always in data_ingestion/scripts/)
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')
)

# Load environment variables from .env in data_ingestion
dotenv_path = os.path.join(project_root, 'data_ingestion', '.env')
load_dotenv(dotenv_path)

EIA_API_KEY = os.getenv("EIA_API_KEY")
if not EIA_API_KEY:
    raise ValueError("EIA_API_KEY not found in .env file.")

# Directory to save raw data
data_dir = os.path.join(project_root, 'data', 'raw')
os.makedirs(data_dir, exist_ok=True)

# Default EIA series IDs for upstream and midstream (monthly data)
SERIES = {
    # Upstream
    'crude_oil_production': 'PET.MCRFPUS2.M',  # U.S. Field Production of
                                               # Crude Oil
    'natural_gas_production': 'NG.N9050US2.M',  # U.S. Natural Gas Gross
                                                # Withdrawals
    'field_production': 'PET.MFPRPUS2.M',  # U.S. Field Production of
                                           # Petroleum
    'crude_oil_reserves': 'PET.RESCRUS1.A',  # U.S. Crude Oil Proved
                                             # Reserves
    'natural_gas_reserves': 'NG.N9051US2.A',  # U.S. Natural Gas Proved
                                              # Reserves
    # Midstream (handled separately for v2)
    'natural_gas_storage': None,  # Placeholder for v2
}

BASE_URL_V1 = "https://api.eia.gov/v2/seriesid/"
BASE_URL_V2_STORAGE = "https://api.eia.gov/v2/natural-gas/storage/data/"


def fetch_eia_series_v1(series_id, api_key):
    url = f"{BASE_URL_V1}{series_id}"
    params = {"api_key": api_key}
    print(f"Fetching {series_id} from v2 backward compatibility API ...")
    resp = requests.get(url, params=params)
    print("Response:", resp.text)  # Debug print
    resp.raise_for_status()
    data = resp.json()
    # Adjusted parsing for v2 response format
    if 'response' in data and 'data' in data['response']:
        df = pd.DataFrame(data['response']['data'])
        return df
    elif 'error' in data:
        raise ValueError(f"API error: {data['error']}")
    else:
        raise ValueError(f"Unexpected response format for {series_id}")


def fetch_natural_gas_storage_v2(api_key):
    print("Fetching natural gas storage from v2 API ...")
    params = {
        "api_key": api_key,
        "facets[region]": "us",
        "frequency": "weekly",
        "data[]": "value"
    }
    resp = requests.get(BASE_URL_V2_STORAGE, params=params)
    print("Response:", resp.text)  # Debug print
    resp.raise_for_status()
    data = resp.json()
    if 'response' in data and 'data' in data['response']:
        df = pd.DataFrame(data['response']['data'])
        return df
    elif 'error' in data:
        raise ValueError(f"API error: {data['error']}")
    else:
        raise ValueError("Unexpected response format for natural gas storage v2")


def fetch_electricity_data(api_key, data_dir, subcategory):
    safe_subcategory = subcategory.replace('/', '_')
    out_path = os.path.join(
        data_dir,
        f"eia_electricity_{safe_subcategory}.csv"
    )
    temp_path = out_path + ".part"
    if os.path.exists(out_path):
        print(f"File {out_path} already exists. Skipping download.")
        return
    print(f"Fetching electricity data from v2 API (subcategory: {subcategory}) ...")
    url = f"https://api.eia.gov/v2/electricity/{subcategory}/data"
    all_data = []
    offset = 0
    length = 5000
    total = None
    first_chunk = True
    try:
        while True:
            params = {
                "api_key": api_key,
                "length": length,
                "offset": offset
            }
            try:
                resp = requests.get(url, params=params)
                print(f"Response for offset {offset}: {resp.text[:200]}...")  # Print first 200 chars
                resp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("HTTPError:", e)
                print("Full response:", resp.text)
                break
            data = resp.json()
            if 'response' in data and 'data' in data['response']:
                chunk = data['response']['data']
                all_data.extend(chunk)
                if chunk:
                    df_chunk = pd.DataFrame(chunk)
                    if first_chunk:
                        df_chunk.to_csv(temp_path, index=False, mode='w')
                        first_chunk = False
                    else:
                        df_chunk.to_csv(temp_path, index=False, mode='a', header=False)
                if total is None:
                    total_val = data['response'].get('total', None)
                    if total_val is not None:
                        total = int(total_val)
                    else:
                        total = None
                if total is not None and total > length:
                    print(f"Fetched {len(chunk)} rows (offset {offset}) of approx. {total}")
                else:
                    print(f"Fetched {len(chunk)} rows (offset {offset})")
                if not chunk or (total is not None and offset + length >= total):
                    break
                offset += length
            elif 'error' in data:
                raise ValueError(f"API error: {data['error']}")
            else:
                raise ValueError("Unexpected response format for electricity data")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Saving partial data...")
        if os.path.exists(temp_path):
            print(f"Partial data saved to {temp_path}")
        else:
            print("No partial data to save.")
        return
    if os.path.exists(temp_path):
        shutil.move(temp_path, out_path)
        print(f"Saved electricity data to {out_path}")
    else:
        print(f"No data fetched for {subcategory}.")


def fetch_petroleum_summary(api_key, data_dir, subcategory):
    safe_subcategory = subcategory.replace('/', '_')
    out_path = os.path.join(
        data_dir,
        f"eia_petroleum_summary_{safe_subcategory}.csv"
    )
    temp_path = out_path + ".part"
    if os.path.exists(out_path):
        print(f"File {out_path} already exists. Skipping download.")
        return
    print(f"Fetching petroleum summary data from v2 API (subcategory: {subcategory}) ...")
    url = f"https://api.eia.gov/v2/petroleum/sum/{subcategory}/data"
    all_data = []
    offset = 0
    length = 5000
    total = None
    first_chunk = True
    try:
        while True:
            params = {
                "api_key": api_key,
                "length": length,
                "offset": offset
            }
            resp = requests.get(url, params=params)
            print(f"Response for offset {offset}: {resp.text[:200]}...")  # Print first 200 chars
            resp.raise_for_status()
            data = resp.json()
            if 'response' in data and 'data' in data['response']:
                chunk = data['response']['data']
                all_data.extend(chunk)
                if chunk:
                    df_chunk = pd.DataFrame(chunk)
                    if first_chunk:
                        df_chunk.to_csv(temp_path, index=False, mode='w')
                        first_chunk = False
                    else:
                        df_chunk.to_csv(temp_path, index=False, mode='a', header=False)
                if total is None:
                    total_val = data['response'].get('total', None)
                    if total_val is not None:
                        total = int(total_val)
                    else:
                        total = None
                if total is not None and total > length:
                    print(f"Fetched {len(chunk)} rows (offset {offset}) of approx. {total}")
                else:
                    print(f"Fetched {len(chunk)} rows (offset {offset})")
                if not chunk or (total is not None and offset + length >= total):
                    break
                offset += length
            elif 'error' in data:
                raise ValueError(f"API error: {data['error']}")
            else:
                raise ValueError("Unexpected response format for petroleum summary")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Saving partial data...")
        if os.path.exists(temp_path):
            print(f"Partial data saved to {temp_path}")
        else:
            print("No partial data to save.")
        return
    if os.path.exists(temp_path):
        shutil.move(temp_path, out_path)
        print(f"Saved petroleum summary data to {out_path}")
    else:
        print(f"No data fetched for {subcategory}.")


def discover_eia_v2_routes(api_key, base_url="https://api.eia.gov/v2"):
    """Discover and print available datasets/routes from the EIA v2 API."""
    print(f"Discovering available datasets at {base_url} ...")
    params = {"api_key": api_key}
    resp = requests.get(base_url, params=params)
    print("Response:", resp.text)  # Debug print
    resp.raise_for_status()
    data = resp.json()
    if 'response' in data and 'routes' in data['response']:
        print("Available routes:")
        for route in data['response']['routes']:
            print(f"- {route}")
        return data['response']['routes']
    elif 'error' in data:
        raise ValueError(f"API error: {data['error']}")
    else:
        raise ValueError("Unexpected response format when discovering routes.")


def explore_eia_v2_tree(api_key, base_url="https://api.eia.gov/v2", prefix="", depth=0, max_depth=5):
    """Recursively explore and print the full tree of available datasets/routes from the EIA v2 API."""
    if depth > max_depth:
        return
    params = {"api_key": api_key}
    try:
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(
            " " * (depth * 2) + f"[Error accessing {base_url}]: {e}"
        )
        return
    if 'response' in data and 'routes' in data['response']:
        routes = data['response']['routes']
        for route in routes:
            # If route is a dict, extract its 'id'; otherwise, use as is
            route_id = route['id'] if isinstance(route, dict) and 'id' in route else str(route)
            print(
                " " * (depth * 2) + f"- {prefix}{route_id}"
            )
            next_url = f"{base_url}/{route_id}"
            next_prefix = prefix + route_id + "/"
            explore_eia_v2_tree(
                api_key,
                next_url,
                prefix=next_prefix,
                depth=depth+1,
                max_depth=max_depth
            )
    elif 'response' in data and 'id' in data['response']:
        # Leaf node, print info
        print(
            " " * (depth * 2) + f"[Leaf] {prefix}{data['response']['id']}"
        )
    elif 'error' in data:
        print(
            " " * (depth * 2) + f"[API error at {base_url}]: {data['error']}"
        )
    else:
        print(
            " " * (depth * 2) + f"[Unexpected response at {base_url}]"
        )


def main():
    print("\nEIA v2 API Dataset Tree:")
    # List of electricity subcategories to download
    electricity_subcategories = [
        "retail-sales",
        "electric-power-operational-data",
        "rto/region-data",
        # State electricity profiles subnodes:
        "state-electricity-profiles/emissions-by-state-by-fuel",
        "state-electricity-profiles/source-disposition",
        "state-electricity-profiles/capability",
        "state-electricity-profiles/energy-efficiency",
        "state-electricity-profiles/net-metering",
        "state-electricity-profiles/meters",
        "state-electricity-profiles/summary",
        "operating-generator-capacity",
        "facility-fuel"
    ]
    # Download all electricity subcategories
    for subcat in electricity_subcategories:
        fetch_electricity_data(EIA_API_KEY, data_dir, subcat)
    # List of petroleum summary subcategories to download
    petroleum_subcategories = [
        "b100",
        #"snd",
        "sndw",
        "crdsnd",
        "mkt"
    ]
    # Download all petroleum summary subcategories
    for subcat in petroleum_subcategories:
        fetch_petroleum_summary(EIA_API_KEY, data_dir, subcat)
    for name, series_id in SERIES.items():
        try:
            if name == 'natural_gas_storage':
                df = fetch_natural_gas_storage_v2(EIA_API_KEY)
            else:
                df = fetch_eia_series_v1(series_id, EIA_API_KEY)
            out_path = os.path.join(
                data_dir,
                f"eia_{name}.csv"
            )
            df.to_csv(out_path, index=False)
            print(
                f"Saved {name} to {out_path}"
            )
        except Exception as e:
            print(
                f"Failed to fetch {name} ({series_id}): {e}"
            )


if __name__ == "__main__":
    main() 