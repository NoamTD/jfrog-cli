from .service import Service
from tabulate import tabulate
import json

def generate_storage_info_table(storage_info_dict):
    def headers(data):
        if type(data) == list:
            return data[0].keys()
        else:
            return data.keys()

    def rows(data):
        if type(data) == list:
            return [x.values() for x in data]
        else:
            return [data.values()]

    binaries = storage_info_dict["binariesSummary"]
    files = storage_info_dict["fileStoreSummary"]
    repositories = storage_info_dict["repositoriesSummaryList"]

    repositories.sort(
        key=lambda x: 1 if x["repoKey"] == "TOTAL" else -1
    )  # Ensure total is the last row

    table = """
Binary storage summary:
{}\n\n
File storage summary:
{}\n\n
Repository storage summary:
{}
    """.format(
        tabulate(rows(binaries), headers(binaries), tablefmt="pretty"),
        tabulate(rows(files), headers(files), tablefmt="pretty"),
        tabulate(rows(repositories), headers(repositories), tablefmt="pretty"),
    )

    return table


class Storage(Service):
    def info(self):
        response = self.requester.get("api/storageinfo", response_is_json=True)
        return generate_storage_info_table(response)