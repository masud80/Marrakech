import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../backend/app/models')
    )
)

from asset_inventory import Asset  # noqa: E402
from __init__ import SessionLocal  # noqa: E402

SAMPLE_ASSETS = [
    {
        'name': 'Apple Inc. Stock',
        'type': 'Equity',
        'value': 150000.0,
        'currency': 'USD',
        'description': 'Shares of Apple Inc.'
    },
    {
        'name': 'US Treasury Bond',
        'type': 'Bond',
        'value': 50000.0,
        'currency': 'USD',
        'description': '10-year US Treasury Bond'
    },
    {
        'name': 'Bitcoin',
        'type': 'Cryptocurrency',
        'value': 30000.0,
        'currency': 'USD',
        'description': 'Holding in Bitcoin'
    },
    {
        'name': 'London Office Building',
        'type': 'Real Estate',
        'value': 2000000.0,
        'currency': 'GBP',
        'description': 'Commercial property in London'
    },
    {
        'name': 'Gold Bullion',
        'type': 'Commodity',
        'value': 100000.0,
        'currency': 'USD',
        'description': 'Physical gold bars'
    },
    {
        'name': 'Offshore Oil Rig - North Sea',
        'type': 'Oil & Gas Asset',
        'value': 50000000.0,
        'currency': 'USD',
        'description': (
            'Deepwater offshore oil drilling platform in the North Sea.'
        )
    },
    {
        'name': 'Natural Gas Pipeline - Texas',
        'type': 'Oil & Gas Asset',
        'value': 12000000.0,
        'currency': 'USD',
        'description': (
            'High-capacity natural gas pipeline in Texas.'
        )
    },
    {
        'name': 'Oil Refinery - Rotterdam',
        'type': 'Oil & Gas Asset',
        'value': 75000000.0,
        'currency': 'EUR',
        'description': (
            'Large-scale oil refinery located in Rotterdam.'
        )
    },
    {
        'name': 'Onshore Drilling Rig - Permian Basin',
        'type': 'Oil & Gas Asset',
        'value': 8000000.0,
        'currency': 'USD',
        'description': (
            'Land-based drilling rig operating in the Permian Basin.'
        )
    },
    {
        'name': 'LNG Storage Facility - Qatar',
        'type': 'Oil & Gas Asset',
        'value': 30000000.0,
        'currency': 'QAR',
        'description': (
            'Liquefied natural gas storage and export facility in Qatar.'
        )
    },
]

def main():
    session = SessionLocal()
    try:
        for asset_data in SAMPLE_ASSETS:
            asset = Asset(**asset_data)
            session.add(asset)
        session.commit()
        print(f"Inserted {len(SAMPLE_ASSETS)} sample assets.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main() 