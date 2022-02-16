import argparse, requests, json, re
from aiohttp import payload
from urllib.parse import urljoin


ADDR_RE = r"0x[a-fA-F0-9]{40}"


def get_payload(label, start, length):
    return {
        "dataTableModel": {
            "draw": 1,
            "columns": [{
                "data": "address",
                "name": "",
                "searchable": True,
                "orderable": False,
                "search": {
                    "value": "",
                    "regex": False,
                },
            }],
            "order": [{
                "column": 1,
                "dir": "asc",
            }],
            "start": start,
            "length": length,
            "search": {
                "value": "",
                "regex": False
            },
        },
        "labelModel": {
            "label": label,
        },
    }


def main(args):
    site = urljoin(args.explorer, "accounts.aspx/GetTableEntriesBySubLabel")

    args.length = min(args.length, 100)

    headers = {
        "Content-Type": "application/json",
        "cookie": f"ASP.NET_SessionId={args.session}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    }
    
    addresses = []
    try:
        while True:
            payload = get_payload(args.label, args.start, args.length)
            response = requests.post(site, headers=headers, data=json.dumps(payload))
            data = response.json()['d']

            for item in data["data"]:
                addresses.append(re.findall(ADDR_RE, item["address"])[0])
            
            args.start += args.length
            if args.start >= data["recordsTotal"]:
                print(json.dumps(addresses))
                return addresses
    except Exception as e:
        print("An exception occurred trying to make the request")
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Etherscan labelcloud fetcher Scrapper")

    parser.add_argument("--label",    "-l", dest="label"  ,  type=str, default="phish-hack", help="Label to fetch")
    parser.add_argument("--amount",   "-a", dest="length",   type=int, default=100, help="Amount of addresses to fetch")
    parser.add_argument("--offset",   "-o", dest="start",    type=int, default=0, help="Offset of addresses to skip")
    parser.add_argument("--session",  "-s", dest="session",  type=str, required=True, help="ASP.NET_SessionId from the explorer cookies")
    parser.add_argument("--explorer", "-e", dest="explorer", type=str, default="https://etherscan.io", help="Etherscan-like explorer url")

    args = parser.parse_args()

    main(args)
