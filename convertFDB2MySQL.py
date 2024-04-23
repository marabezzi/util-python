import fdb
import mysql.connector
import schedule
import time

def convert_firebird_to_mysql(firebird_host, firebird_database, firebird_user, firebird_password,
                              mysql_host, mysql_database, mysql_user, mysql_password):
    try:
        # Conecta ao banco de dados Firebird
        firebird_conn = fdb.connect(
            host=firebird_host,
            database=firebird_database,
            user=firebird_user,
            password=firebird_password
        )

        # Conecta ao banco de dados MySQL
        mysql_conn = mysql.connector.connect(
            host=mysql_host,
            database=mysql_database,
            user=mysql_user,
            password=mysql_password
        )

        # Cria cursores para ambos os bancos de dados
        firebird_cursor = firebird_conn.cursor()
        mysql_cursor = mysql_conn.cursor()

        # Obter todas as tabelas do banco de dados Firebird
        firebird_cursor.execute("SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0")
        tables = firebird_cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # Obter as colunas da tabela
            firebird_cursor.execute(f"SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS WHERE RDB$RELATION_NAME = '{table_name}'")
            columns = [column[0] for column in firebird_cursor.fetchall()]
            
            # Obter as chaves primárias da tabela
            firebird_cursor.execute(f"SELECT i.RDB$FIELD_NAME FROM RDB$INDICES i JOIN RDB$INDEX_SEGMENTS s ON i.RDB$INDEX_NAME = s.RDB$INDEX_NAME WHERE i.RDB$RELATION_NAME = '{table_name}' AND i.RDB$INDEX_TYPE = 1")
            primary_keys = [pk[0] for pk in firebird_cursor.fetchall()]
            
            # Criar a tabela no MySQL
            create_table_query = f"CREATE TABLE {table_name} ("
            for column in columns:
                create_table_query += f"{column} VARCHAR(255), "
            create_table_query += f"PRIMARY KEY ({', '.join(primary_keys)})" if primary_keys else ""
            create_table_query += ")"
            mysql_cursor.execute(create_table_query)

            # Inserir dados na tabela MySQL
            firebird_cursor.execute(f"SELECT * FROM {table_name}")
            for row in firebird_cursor.fetchall():
                mysql_cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})", row)
        
        # Commit as alterações no banco de dados MySQL
        mysql_conn.commit()

        # Fecha as conexões
        firebird_conn.close()
        mysql_conn.close()
        print("Conversão concluída com sucesso!")

    except Exception as e:
        print(f"Erro durante a conversão: {e}")

def convert_and_schedule():
    convert_firebird_to_mysql(
        firebird_host='localhost',
        firebird_database='firebird_db',
        firebird_user='firebird_user',
        firebird_password='firebird_password',
        mysql_host='localhost',
        mysql_database='mysql_db',
        mysql_user='mysql_user',
        mysql_password='mysql_password'
    )

# Agendar a conversão para ser executada a cada 24 horas
schedule.every(24).hours.do(convert_and_schedule)

# Loop principal para manter o script em execução
while True:
    schedule.run_pending()
    time.sleep(1)
