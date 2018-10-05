import watson_developer_cloud
import json
import ibm_db
from ibm_db import fetch_assoc, tables, exec_immediate

def watsonConnection(message, context, categoria):
    user = 'fe0ed9e8-fd96-405b-baee-3a0e8e6e95b1'
    pw = 'TPKMPYH21L3Q'
    wk = ''
    if(categoria == 'st'):
        wk = '85a2b90e-4d6c-42ef-9787-e269d38f2aad'
    else:
        wk = 'fc9f117a-f372-4f93-b932-bade81508504'
    assistant = watson_developer_cloud.AssistantV1(
        username=user,
        password=pw,
        version='2018-09-25'
    )
    print(context)
    response = assistant.message(
        workspace_id=wk,
        encoding='utf-8',
        input={
            'text': message
        },
		context= eval(context)
    ).get_result()

    return response


def insertarUsuarios(tx_usuario,tx_nombre):
    # Documentacion python - bbdd en https://www.ibm.com/support/knowledgecenter/es/SSEPGG_9.5.0/com.ibm.db2.luw.apdv.python.doc/doc/t0054388.html
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=jnw52971;PWD=ft0d3qpf+q1whs7n;", "", "")
    sql = "INSERT INTO JNW52971.T_USUARIOS(TX_USUARIO,TX_NOMBRE) VALUES('" + tx_usuario +"','" + tx_nombre +"')"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    """dictionary = ibm_db.fetch_both(stmt)
    output = ""
    while dictionary != False:
        output += str(dictionary['ID_USER']) + " - " + str(dictionary['NOMBRE_USUARIO']) + "<br>"
        dictionary = ibm_db.fetch_both(stmt)
    """
    ibm_db.close(conn)

    if stmt:
        return "ok"
    else:
        return "error"

def insertarAnalisis(id_usuario,co_tipo_analisis,fe_fecha_analisis):
     # Documentacion python - bbdd en https://www.ibm.com/support/knowledgecenter/es/SSEPGG_9.5.0/com.ibm.db2.luw.apdv.python.doc/doc/t0054388.html
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=jnw52971;PWD=ft0d3qpf+q1whs7n;", "", "")
    sql = "INSERT INTO JNW52971.T_ANALISIS(ID_USUARIO,CO_TIPO_ANALISIS,FE_FECHA_ANALISIS) VALUES('" + id_usuario +"','" + co_tipo_analisis +"','" + fe_fecha_analisis + "')"

    stmt = ibm_db.exec_immediate(conn, sql)

    ibm_db.close(conn)

    if stmt:
        return "ok"
    else:
        return "error"   
def updateAnalisis(id_usuario,co_tipo_analisis,fe_fecha_analisis):
	return "ok"