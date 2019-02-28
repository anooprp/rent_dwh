import pandas as pd
from pandas.io.json import json_normalize
from rent_dwh.util import get_postgres_con,get_columns_postgres
import os



class RentData(object):


    def __init__(self):

        self.file_loc="/data/CSV/"


    def load_data_from_file(self):

        mf=pd.read_json(self.input_filename, lines=True)

        data_points=list(mf['data'])

        self.main_df = json_normalize(data_points)




    def export_to_file(self,column_list,target_table,delim='|'):


        table_df = pd.DataFrame()
        table_df[column_list]=self.main_df[column_list]

        self.filename=self.file_loc+"{fname}.csv".format(fname=target_table)

        self.table_df=table_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True)
        self.table_df.to_csv(self.filename, sep=delim, header=True, index=False, encoding='utf-8')

    def postgres_data_load(self, table_name, file_name, trunc_flag='N', delim=','):
        conn=get_postgres_con()
        SQL_STATEMENT = """
            COPY {tab_name} FROM STDIN WITH
                CSV 
                HEADER
                NULL AS ''
                QUOTE '"'
                DELIMITER AS '{delim}'
            """.format(tab_name=table_name, delim=delim)
        my_file = open(file_name)

        cursor = conn.cursor()
        if trunc_flag == 'Y':
            print(" Truncating table before load " + table_name)
            cursor.execute(" truncate table " + table_name)

        cursor.copy_expert(sql=SQL_STATEMENT, file=my_file)
        conn.commit()
        cursor.close()
        conn.close()

        self.stage_table = table_name





    def target_data_load(self,target_table,unique_id):
        conn = get_postgres_con()
        cursor = conn.cursor()
        if unique_id:
            print('Deleting data from target')
            del_sql="""delete from {tar_table} where ({uni_id})
                        in (select {uni_id} from {stg_table})""".\
                format(tar_table=target_table,uni_id=unique_id,stg_table=self.stage_table)
            print(del_sql)
            cursor.execute(del_sql)
        v_columns = get_columns_postgres(target_table)
        ins_sql="""insert into {tar_table}({columns}) select ({columns}) from {stg_table}""".\
            format(tar_table=target_table,stg_table=self.stage_table,columns=v_columns)
        print(ins_sql)
        cursor.execute(ins_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def __del__(self):
        if os.path.exists(self.filename):
            print(' File removed ')
            os.remove(self.filename)


