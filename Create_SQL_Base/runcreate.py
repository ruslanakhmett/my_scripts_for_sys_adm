import subprocess
import time
from Add_to_MSSQL import req_sql


passes_ms_sql = {
          '1sql01': 'passpass123',
          '1sql02': 'passpass123',
          '1sql03': 'passpass123',
          '1sql04': 'passpass123',
          '1sql05': 'passpass123',
          '1sql06': 'passpass123',
          '1sql07': 'passpass123',
          '1sql08': 'passpass123'
}

users_ms_sql = {
         '1sql01': 'user',
         '1sql02': 'user',
         '1sql03': 'user',
         '1sql04': 'user',
         '1sql05': 'user',
         '1sql06': 'user',
         '1sql07': 'user',
         '1sql08': 'user'
}

users_cluster = {
         '1sql01': 'user',
         '1sql02': 'user',
         '1sql03': 'user',
         '1sql04': 'user',
         '1sql05': 'user',
         '1sql06': 'user',
         '1sql07': 'user',
         '1sql08': 'user'
}

passes_cluster = {
          '1sql01': 'passpass123',
          '1sql02': 'passpass123',
          '1sql03': 'passpass123',
          '1sql04': 'passpass123',
          '1sql05': 'passpass123',
          '1sql06': 'passpass123',
          '1sql07': 'passpass123',
          '1sql08': 'passpass123'
}

base_name = input('Enter db name (id99999-baseX): ')
disk_letter = input('Enter disk letter (X): ')
server_name = input('Enter server name (1sql0X): ')
base_name_for_list = input('Enter base name for list: (InfoBaseX): ')
tasks_block = 'N'
pwd_ms_sql = passes_ms_sql[server_name]
user_ms_sql = users_ms_sql[server_name]
user_cluster = users_cluster[server_name]
pwd_cluster = passes_cluster[server_name]


req_sql(server_name, base_name, pwd_ms_sql, disk_letter, user_ms_sql)

create_db_cmd = f'CREATEINFOBASE Srvr={server_name};' \
                f'Ref={base_name};' \
                'DBMS=MSSQLServer;' \
                f'DBSrvr={server_name};' \
                f'DB={base_name};' \
                f'DBUID={user_cluster};' \
                f'DBPwd={pwd_cluster};' \
                'SQLYOffs=2000;' \
                f'SchJobDn={tasks_block}; ' \
                f'/AddInList {base_name_for_list}'

process_create = subprocess.Popen([r"C:\Program Files (x86)\1cv8\8.3.18.1289\bin\1cv8.exe", create_db_cmd])

print('All is ready')
time.sleep(6)


