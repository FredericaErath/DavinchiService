"""
Define all the constants here.
"""
import os.path

BASE_DIR = 'F:/DavinciService/'
BASE_CORE_DIR = os.path.join(BASE_DIR, 'core/')
BASE_DATA_DIR = os.path.join(BASE_CORE_DIR, 'data/')
BASE_DATA_TEMP_DIR = os.path.join(BASE_DATA_DIR, 'TEMP/')
USER_DICT_REVERSE = {1: "医生", 2: "护士", 0: "管理员"}
USER_COLUMNS = {"账号": "u_id", "用户名称": "name", "用户类型": "user_type", "密码": "code"}
INSTRUMENT_COLUMNS = {"器械名称": "i_name", "使用次数": "times"}
DC_INSTRUMENT_TO_SUPPLY = {"电剪": "尖端盖附件"}
DC_SUPPLY_TO_NUMBER = {"无菌壁套": 4, "中心柱无菌套": 1, "尖端盖附件": 1}
USER_DICT = {"医生": 1, "护士": 2, "管理员": 0}
DC_DEPARTMENT = {"肝脾外科": "hepa", "胃肠外科": "gastro",
                 "泌尿外科": "urologic", "胆胰外科": "pancreatic",
                 "胸外科": "chest", "妇科": "gynae", "心脏外科": "cardiac"}
LS_PART = ["机器人援助下肺病损切除", "机器人援助下半肝切除术", "机器人援助下肾部分切除术", "机器人援助下肾根治性切除术",
           "机器人援助下肾上腺肿瘤切除", "机器人援助下肾切开取石术", "机器人援助下输尿管膀胱吻合术",
           "机器人援助下输尿管狭窄段切除吻合术"]
