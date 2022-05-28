import mysql.connector

def connector_():
    database_connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="admin",
        database="queries"
        )
    return database_connection


def dataReader():
    resultArray = []
    database = connector_()
    cursor_ = database.cursor()
    cursor_.execute("SELECT * FROM querys")
    result = cursor_.fetchall()
    for entrys in result:
        print(entrys)
    return result

def readStatments():
    resultArray = []
    database = connector_()
    cursor_ = database.cursor()
    cursor_.execute("SELECT * FROM statments")
    result = cursor_.fetchall()
    '''for entrys in result:
        print(entrys)'''
    return result


def databaseInsertion(solution,querynumber,description):
    database = connector_()
    cursor_ = database.cursor()
    statment = "INSERT INTO queries (graph, querynumber, description) VALUES (%s, %s, %s)"
    values = (str(solution),str(querynumber), description)
    cursor_.execute(statment, values)
    database.commit()
    database.close()
    pass

def statmentInsertion(graph, querynumber, statment):
    database = connector_()
    cursor_ = database.cursor()
    graphEntrysReader = dataReader()
    for i in graphEntrysReader:
        if graph == i[0] and querynumber == i[1]:
           insert_statment = "INSERT INTO statments (querynumber, statment) VALUES (%s, %s)"
           values = (str(querynumber), str(statment))
           cursor_.execute(insert_statment, values)
           print("statment addes!")
           database.commit()
           database.close()
           return True

    database.close()
    print("Ther is no solution ", graph, " or querynumber", querynumber, "")
    return False
    pass


if __name__=="__main__":

    pass