import os.path
from datetime import datetime
from typing import Union
import numpy as np
from fastapi import HTTPException

from constant import INSTRUMENT_COLUMNS, BASE_DATA_TEMP_DIR
from core.database import get_instrument, update_instrument, delete_instrument, insert_instrument
import pandas as pd

from core.utils import pack_files


def get_all_instrument():
    """
    Get all instruments.
    """
    instruments = get_instrument()
    if len(instruments) == 0:
        return []
    else:
        df = pd.DataFrame(instruments)[["i_id", "i_name", "times", "insert_time"]]
        conditions = [(df['times'] <= 0), (df['times'] > 0)]
        values = ['失效', '有效']
        df["validity"] = np.select(conditions, values)
        return df.to_dict('records')


def get_instrument_general(begin_time: datetime | None = None,
                           end_time: datetime | None = None,
                           i_id: int | list[int] | None = None,
                           i_name: str | list[str] | None = None,
                           times: int | list[int] | None = None,
                           validity: bool = None):
    """
    Get instruments based on different parameters
    """
    instruments = get_instrument(begin_time=begin_time, end_time=end_time, i_id=i_id, i_name=i_name, times=times,
                                 validity=validity)
    if len(instruments) == 0:
        return []
    else:
        df = pd.DataFrame(instruments)[["i_id", "i_name", "times", "insert_time"]]
        return df.to_dict('records')


def revise_instrument(i_id: int,
                      times: int):
    """
    Revise instrument times
    """
    res = update_instrument(i_id=i_id, v_times=times)
    if res == "unsuccessful":
        raise HTTPException(status_code=500, detail="Something went wrong")
    else:
        return res


def download_instrument_qr_code(i_id: int):
    """
    Download one qr_code.
    """
    f_path = os.path.join(BASE_DATA_TEMP_DIR, f'{str(i_id)}.png')
    if os.path.exists(f_path):
        return f_path
    else:
        try:
            qr_code = get_instrument(i_id=i_id)[0]["qr_code"]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Can't find instrument{str(i_id)}, and raise: {e}")
        with open('temp.png', 'wb') as fp:
            fp.write(qr_code)
        return "temp.png"


def add_instruments_by_file(f_instruments: str):
    """
    Add instruments by excel.
    """
    res = {}
    df = pd.read_excel(f_instruments, engine='openpyxl')
    columns = df.columns.tolist()
    if columns == ["器械名称"] or columns == ["i_name"]:
        res = insert_instrument(df[columns[0]].tolist())
    # check columns
    elif set(columns) == set(INSTRUMENT_COLUMNS.values()):
        df = df.rename(columns=INSTRUMENT_COLUMNS)
        res = insert_instrument(df[columns[0]].tolist(), df[columns[1]].tolist())
    else:
        HTTPException(status_code=400, detail="Columns do not fit for restriction.")
    if res["msg"] == "unsuccessful":
        raise HTTPException(status_code=400, detail="upload operation failed")
    else:
        return pack_files(res["files"])


def add_one_instrument(i_name: str, times: int = None):
    """
    Add one instrument into database.
    """
    res = insert_instrument(i_name=i_name, times=times)
    if res["msg"] == "unsuccessful":
        raise HTTPException(status_code=400, detail="upload operation failed")
    else:
        return {"file": res["files"][0], "file_name": res["file_name"]}


def delete_instruments_by_id(i_id: Union[int, list[int]]):
    """
    Delete one or many instruments by instrument id.
    """
    res = delete_instrument(i_id=i_id)
    if res == "unsuccessful":
        raise HTTPException(status_code=500, detail="Something went wrong")
    else:
        return res
