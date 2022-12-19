from openpyxl import load_workbook
from pathlib import Path
import logging
import json
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"


def load_file(excel_file=BASE_DIR / 'helpers' / 'test.xlsx'):
    """Load bundles store in an Excel file into json with the name of each sheet.
    Each bundle's operator is store in a sheet with the heading:
     ---------------------------------------------
    | Name | Sms | Call | Data | Validity | Price |
     ---------------------------------------------

    Args: excel_file (str, optional): Excel file containing differents bundles' operator per sheet.
    Defaults to 'test.xlsx'.
    """

    # Storage creation
    shutil.rmtree(STORAGE_DIR, ignore_errors=True)
    STORAGE_DIR.mkdir(exist_ok=True)

    logging.basicConfig(level=logging.DEBUG,
                        filename=BASE_DIR / "api.log",
                        filemode="w",
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # load the spreadsheet
    wb = load_workbook(excel_file)

    for sheetname in wb.sheetnames:

        sheet = wb[sheetname]

        # Operator bundle empty file creation
        bundle_file = STORAGE_DIR / f"{sheetname.lower().replace(' ', '_')}.json"
        bundle_file.touch()
        bundle_file.write_text("{}")
        logging.info("Empty bundle file created.")

        row_count = sheet.max_row
        column_count = sheet.max_column

        headers = ["name", "sms", "call", "data", "validity", "price"]
        with open(bundle_file, 'r') as f:
            bundles = json.load(f)

        for i in range(2, row_count + 1):
            bundle = {}
            maximum = 0
            for j in range(1, column_count + 1):
                data = sheet.cell(row=i, column=j).value

                # reformat data cells from str to int according to Mo or Go
                if j == 4:
                    try:
                        data_temp = data.split(" ")
                        if data_temp[1]:
                            bundle["data"] = int(float(data_temp[0].replace(",", ".")) * 1000)
                    except AttributeError:
                        bundle["data"] = data

                # reformat validity from str to int removing "jours"
                if j == 5:
                    try:
                        data_temp = data.split(" ")
                        if data_temp[1]:
                            data = int(data_temp[0])
                    except IndexError:
                        logging.debug("No 'jours' string on this validity.")

                # Add line's values in a dict
                if j != 4:
                    bundle[headers[j - 1]] = data

            # Add bundle info in the dict of bundles
            key = bundle.pop('name')
            bundles[key] = bundle.copy()

            # Sort the bundle items and assign them priorities
            del bundle['price'], bundle['validity']

            sorted_bundle_items = dict(sorted(bundle.items(), key=lambda item: item[1], reverse=True))

            for val in sorted_bundle_items.values():
                maximum = val
                break

            priorities = []
            for k, v in sorted_bundle_items.items():
                val = v / maximum
                sorted_bundle_items[k] = val
                priorities.append(val)

            # Definition of an item priority in the bundle
            if priorities[0] == priorities[1]:
                if priorities[2] != 0 and priorities[2] != 1:
                    priorities[2] = 2
            elif priorities[1] == priorities[2] and priorities[1] != 0:
                priorities[1] = priorities[2] = 2
            elif priorities[1] == priorities[2] and priorities[1] == 0:
                pass
            else:
                priorities[1] = 2
                priorities[2] = 3

            for k in range(0, 3):
                priorities[k] = int(priorities[k])

            priority_counter = 0
            for k, v in sorted_bundle_items.items():
                sorted_bundle_items[k] = priorities[priority_counter]
                priority_counter += 1

            bundles[key]["priorities"] = sorted_bundle_items

            with open(bundle_file, "w", encoding="utf-8") as f:
                json.dump(bundles, f, indent=4, ensure_ascii=False)
            logging.info(f"Bundle {key} of {sheetname} saved.")


if __name__ == "__main__":
    load_file()
    logging.debug("Load datas test passed.")
