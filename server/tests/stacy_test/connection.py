import server.model.connection as smc

def test_connection_string():
    res = smc.create_conn_string()
    print()
    print(res)