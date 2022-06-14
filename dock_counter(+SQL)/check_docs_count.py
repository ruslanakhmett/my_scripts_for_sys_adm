import psycopg2
from datetime import datetime, timedelta


file = open('sn_for_check_docs_count','r')
list_kkt = []
for line in file:
    if line != '\n':
        list_kkt.append(line.strip())

days_period = input('For last days(empty for all days): ')

string_for_query = ''
for item in list_kkt:
    string_for_query += f"('{item}'), " #собираем строку для передачи в запрос вида (item), (item), 

if days_period:
    now_date = datetime.now()
    result_date = now_date.date() - timedelta(days=int(days_period))
    
    query_get_count = f'''WITH sn_list AS (VALUES {string_for_query[:-2]})  
                    SELECT doc."DeviceSN", doc."FSNumber",
                    org."Name" AS "OrgName",
                    gr."Name" AS "GroupName",
                    COUNT(doc."ExternalId") as DocsCount,
                    MAX(doc."ReceivedAt") as "LastDockDate"
                    FROM "Documents" as doc
                    INNER JOIN "Organizations" AS org ON doc."OrganizationId" = org."Id"
                    INNER JOIN "DeviceGroups" AS gr ON gr."Id" = doc."DeviceGroupId"
                    WHERE  doc."DeviceSN" in (SELECT * FROM sn_list) AND "ReceivedAt" > '{result_date}'
                    GROUP BY doc."FSNumber", doc."DeviceSN",gr."Name",org."Name"
                    ORDER BY doc."DeviceSN"'''
else:
    query_get_count = f'''WITH sn_list AS (VALUES {string_for_query[:-2]})
                    SELECT doc."DeviceSN", doc."FSNumber",
                    org."Name" AS "OrgName",
                    gr."Name" AS "GroupName",
                    COUNT(doc."ExternalId") as DocsCount,
                    MAX(doc."ReceivedAt") as "LastDockDate"
                    FROM "Documents" as doc
                    INNER JOIN "Organizations" AS org ON doc."OrganizationId" = org."Id"
                    INNER JOIN "DeviceGroups" AS gr ON gr."Id" = doc."DeviceGroupId"
                    WHERE  doc."DeviceSN" in (SELECT * FROM sn_list)
                    GROUP BY doc."FSNumber", doc."DeviceSN",gr."Name",org."Name"
                    ORDER BY doc."DeviceSN"'''

try:
    connection = psycopg2.connect(
        host="host_name",
        database="database_name",
        user="user_name",
        password="passwd",
        port='port')

    cursor = connection.cursor()
    print('Please, wait...')
    cursor.execute(query_get_count)

    recieved_data = cursor.fetchall()

    if recieved_data:
        for row in recieved_data:
            print('..........................................')
            print("SN:", row[0], " FN:", row[1])
            print("OrgName:", row[2], " GroupName:", row[3])
            if days_period:
                print(f'docsCount for last {days_period} days: ', row[4])
            else:
                print(f'docsCount for ALL days: ', row[4])
            print("LastDocDate:", row[5])
    else:
        print('..........................................')
        print('Not found')

except (Exception, psycopg2.Error) as error:

    print("Error while fetching data from PostgreSQL", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("\nPostgreSQL connection is closed")
