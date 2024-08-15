import argparse
import traceback

from constants import company_internal_db, output_types
import importlib
from utils import get_webdriver, print_data


def process_ids(company_ids_list=None, output_type: str = "csv"):
    if company_ids_list is None:
        # process all ids
        company_ids_list = list(company_internal_db.keys())

    processed_objs = []
    driver = get_webdriver()
    for cid in company_ids_list:
        # From company name construct class name dynamically and load it
        name = "".join(company_internal_db.get(cid)[0].split(" "))
        module = importlib.import_module(f"clients.{name.lower()}")
        class_ = getattr(module, name)
        obj = class_(cid,
                     company_internal_db[cid][0],
                     company_internal_db[cid][1],
                     output_type,
                     driver)

        print(f"Processing: {obj.name}")
        try:
            obj.process()
            processed_objs.append(obj)
        except Exception as ex:
            print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))

    driver.quit()

    print("processed_objs:", processed_objs)
    if processed_objs:
        print_data(processed_objs, output_type)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--ids', help='comma delimited company ids', type=str)
    parser.add_argument('-o', '--output', help='Supported output types:csv/json', type=str)
    args = parser.parse_args()

    # Parse ids
    company_ids_list = None
    if args.ids:
        company_ids_list = [item for item in args.ids.split(',')]

        # Validate company ids against internal db
        company_ids = company_internal_db.keys()
        found = []
        for cid in company_ids_list:
            if cid not in company_ids:
                found.append(cid)

        if found:
            print(f"company ids {found} not found in internal DB. Update DB with required details.")
            exit(1)
    print("company_ids_list:", company_ids_list)

    # Parse output type
    output = "csv"
    if args.output:
        output = args.output

        # validate output type
        if output not in output_types:
            print(f"Provided output format not supported. Supported formats are {output_types}")
            exit(1)

    print("output:", output)

    process_ids(company_ids_list, output)


if __name__ == '__main__':
    main()
