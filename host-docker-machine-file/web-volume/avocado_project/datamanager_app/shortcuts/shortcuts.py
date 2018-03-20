import pandas as pd
from datetime import datetime

from . import models

## shortcuts.py
## views.py 에서 사용할 db, authorization, permission, data processing 등의 다양한 logic 을 구현합니다

class KppExcelReader():
    '''
    KppExcelReader

    정해진 Excel 형식만 받는 KppPalletData Model 을 위한 excel to db reader

    사용법
    1. initalize a instance ... KppExcelReader(filepath[string], sheets[list of strings])
    2. validate excel using ... is_valid()
    3. if it returns False, tell user to upload again with proper excel form
    4. pusj code to db using ... push_only_code()
    5. push data to db using ... push_to_db()


    '''
    def __init__(self, filepath, sheets):
        self.filepath = filepath # xlsx filepath : string
        self.sheets = sheets #sheet lists
        self.df_list = self._excel_to_df()

    def _excel_to_df(self):
        df_list = []
        for sheet in self.sheets :
            df = pd.read_excel(self.filepath, sheet)
            df_list.append(df)

        return df_list

    def _make_onecol_list(self,col):
        result = set()
        for df in self.df_list:
            result = set(list(result) + list(set(df[col])))

        return list(result)

    # Check columns contain ["타입","코드","발송일","유형","수량"]
    def is_valid(self):
        for df in self.df_list:
            col_set = set(list(df))
            if len(col_set - {'타입','코드','발송일','유형','수량'}) != (len(col_set)-5) :
                return False

        return True

    # Push code data to model Code
    def push_only_code(self, col="코드"):
        model = models.Code
        code_list = self._make_onecol_list(col)

        for c in code_list :
            if not list(model.objects.get(code=str(c))):
                code = model(code=str(c))
                code.save()

    # Push Dataframe data to Database(Model)
    def push_to_db(self):
        model = models.KppPalletData
        col_order = ["타입", "코드", "발송일", "유형", "수량"]

        for df in self.df_list :
            compact = df[list(col_order)]

            long = len(df)
            for i in range(long):
                row = list(compact.iloc[i])
                type = str(row[0])
                code = str(row[1])
                date = datetime(int(str(row[2])[:4]), int(str(row[2])[4:6]),int(str(row[2])[6:]))
                palletcode = str(row[3])
                pallet = row[4]

                try:
                    # get 이 에러를 발생시킴 (만약 존재하지 않는다면)
                    exsist = models.KppPalletData.objects.filter(date=date).filter(palletcode=palletcode).get(
                        pallet=pallet)
                    exsist.code = code
                    exsist.save()

                except:
                    pallet_data = models.KppPalletData(type=type, code=code, date=date, palletcode=palletcode,
                                                       pallet=pallet)
                    pallet_data.save()








