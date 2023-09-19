"""
Define all the constants here.
"""
import os.path

BASE_DIR = 'F:/DavinciService/'
BASE_CORE_DIR = os.path.join(BASE_DIR, 'core/')
BASE_DATA_DIR = os.path.join(BASE_CORE_DIR, 'data/')
BASE_DATA_TEMP_DIR = os.path.join(BASE_DATA_DIR, 'temp/')
USER_DICT_REVERSE = {1: "医生", 2: "护士", 0: "管理员"}
USER_COLUMNS = {"账号": "u_id", "用户名称": "name", "用户类型": "user_type", "密码": "code"}
INSTRUMENT_COLUMNS = {"器械名称": "i_name", "使用次数": "times"}
DC_INSTRUMENT_TO_SUPPLY = {"电剪": "尖端盖附件"}
DC_SUPPLY_TO_NUMBER = {"无菌壁套": 4, "中心柱无菌套": 1, "尖端盖附件": 1}
USER_DICT = {"医生": 1, "护士": 2, "管理员": 0}
DC_DEPARTMENT = {"肝脾外科": "hepa", "胃肠外科": "gastro", "泌尿外科": "urologic", "胆胰外科": "pancreatic",
                 "胸外科": "chest", "妇科": "gynae", "心脏外科": "cardiac"}
DC_DEPARTMENT_REVERSE = {'hepa': '肝脾外科', 'gastro': '胃肠外科', 'urologic': '泌尿外科', 'pancreatic': '胆胰外科',
                         'chest': '胸外科', 'gynae': '妇科', 'cardiac': '心脏外科'}
LS_PART = ["肺病损切除", "半肝切除术", "肾部分切除术", "肾根治性切除术",
           "肾上腺肿瘤切除", "肾切开取石术", "输尿管膀胱吻合术",
           "输尿管狭窄段切除吻合术"]
PRICE_MAP = {"卡迪亚": 3437.9, "马里兰": 4420.1, "电剪": 5238.7, "细持": 3601.6, "双极无损": 4420.1, "超声刀": 8922.2,
             "尖端盖附件": 233.7, "无菌壁套": 233.7, "中心柱无菌套": 233.7}

