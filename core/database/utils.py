import pandas as pd

from core.database.base import davinci_db


def get_empty_df(collection: str):
    """Return an empty list with columns when we can't find any data in database."""
    cols = list(davinci_db.command(
        {'listCollections': 1, 'filter': {'name': collection}})["cursor"]["firstBatch"][0]["options"]["validator"][
        "$jsonSchema"]["properties"].keys())
    return list(pd.DataFrame(cols))

