import argparse
import json
import os
import urllib.request
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def platform_code_generator(platform):
    code_generator = dict(
        tradingview=lambda x: f"{x['exch_seg']}:{x['name']}",
        dhan=lambda x: f"{x['exch_seg']}E{x['token']}:{x['name']}"
    )
    return code_generator[platform.lower()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="file of TradingView Watchlist in .txt format",
                        type=str, required=True)
    parser.add_argument("--platform", help="Platform to convert your watchlist to. dhan only supported right now.",
                        type=str, default="dhan", required=False)
    parser.add_argument("--exchange_data_file", help="exchange code data file (json)",
                        type=str, default="OpenAPIScripMaster.json", required=False)
    args = parser.parse_args()

    if not os.path.exists(args.exchange_data_file):
        os.system("wget https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")
        args.exchange_data_file = "OpenAPIScripMaster.json"

    with open(args.exchange_data_file, 'r') as f:
        exchange_code_data = pd.DataFrame(json.loads(f.read()))

    # select the data only for NSE and BSE
    exchange_code_data = exchange_code_data[exchange_code_data["exch_seg"].isin(['NSE', 'BSE'])]

    # select only equity segment
    exchange_code_data[["symbol", "segment"]] = exchange_code_data["symbol"].str.split("-", 1, expand=True)
    exchange_code_data = exchange_code_data[exchange_code_data["segment"].isin(['EQ', 'SM'])]

    exchange_code_data["tradingview_code"] = exchange_code_data.apply(platform_code_generator("tradingview"), axis=1)
    exchange_code_data[f"{args.platform.lower()}_code"] = exchange_code_data.apply(platform_code_generator(args.platform.lower()), axis=1)

    # open the input trading view file
    with open(args.file, "r") as f:
        tradingview_watchlist = f.read()

    tradingview_watchlist = tradingview_watchlist.split(",")
    logging.info(f"There are {len(set(tradingview_watchlist))} stocks in the input watchlist")

    output_data = exchange_code_data[exchange_code_data["tradingview_code"].isin(tradingview_watchlist)]
    output_watchlist_codes = output_data[f"{args.platform}_code"].values.tolist()
    logging.info(f"{len(output_watchlist_codes)} stock codes have been converted for {args.platform.upper()} platform.")
    output_txt = ",".join(output_watchlist_codes)

    new_file = f"{args.platform}_{args.file}"
    with open(new_file, "w") as f:
        f.write(output_txt)

    logging.info(f"Saved watchlist for {args.platform.upper()} platform as {new_file}.")

    diff = set(tradingview_watchlist) - set(output_data["tradingview_code"])
    if len(diff) > 0:
        logging.warning(f"Following Stocks couldn't be mapped to {args.platform.upper()} - {','.join(list(diff))}. Try adding them manually")













