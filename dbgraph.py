from neo4j import GraphDatabase
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

# Метод, который передает запрос в БД
    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

conn = Neo4jConnection(uri="bolt://localhost:7687",user="Wassim",password="Wassim2002")

#LOAD TABLES
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Tables.csv'
AS line FIELDTERMINATOR ','
MERGE (table:Tables {tableId: line.TableId})
  ON CREATE SET table.tableName = line.TableName;
'''
conn.query(query_string, db='graphDb')
#LOAD CHAIRS
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Chairs.csv'
AS line FIELDTERMINATOR ','
MERGE (chair:Chairs {chairId: line.ChairID})
  ON CREATE SET chair.chairName = line.ChairName;
'''
conn.query(query_string, db='graphDb')

#LOAD WINDOWS
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Window.csv'
AS line FIELDTERMINATOR ','
MERGE (window:Window {windowId: line.WindowID})
  ON CREATE SET window.windowName = line.WindowName;
'''
conn.query(query_string, db='graphDb')

#LOAD DESK
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Desk.csv'
AS line FIELDTERMINATOR ','
MERGE (desk:Desk {deskId: line.DeskId})
  ON CREATE SET desk.deskName = line.DeskName;
'''
conn.query(query_string, db='graphDb')

#LOAD CHALK
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Chalk.csv'
AS line FIELDTERMINATOR ','
MERGE (chalk:Chalk {chalkId: line.ChalkID})
  ON CREATE SET chalk.chalkName = line.ChalkName;
'''
conn.query(query_string, db='graphDb')


#LOAD DOOR
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Door.csv'
AS line FIELDTERMINATOR ','
MERGE (door:Door {doorId: line.DoorID})
  ON CREATE SET door.doorName = line.DoorName;
'''
conn.query(query_string, db='graphDb')

#LOAD CLASS
query_string = '''
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Class.csv'
AS line FIELDTERMINATOR ','
MERGE (class:Class {classId: line.ClassId})
  ON CREATE SET class.classNumber = line.ClassNumber;
'''
conn.query(query_string, db='graphDb')


#CREATE RELATIONSHIP BETWEEN TABLES AND CHAIRS WITH CLASS(IS_IN) AND TABLES WITH EACH OTHERS(ON_THE_LEFT)
query_string = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Equipement.csv' AS line
MATCH (class:Class {classId: line.ClassId})

// Create tables and chairs with unique identifiers with UNWIND
UNWIND RANGE(1, 10) AS tableNumber
MERGE (table:Tables {tableId: toString(tableNumber)})
MERGE (chair:Chairs {chairId: toString(tableNumber)})

// Create relationships between tables and chairs and the class
CREATE (table)-[:IS_IN]->(class)
CREATE (chair)-[:IS_IN]->(class)

// Create relationships between tables
WITH collect(table) AS tables
FOREACH (i IN RANGE(0, size(tables) - 2) |
  FOREACH (table1 IN [tables[i]] |
    FOREACH (table2 IN [tables[i+1]] |
      CREATE (table1)-[:ON_THE_LEFT]->(table2)
    )
  )
)


'''
conn.query(query_string, db='graphDb')
#CREATE RELATIONSHIPS BETWEEN WINDOW1,DESK AND DOOR
query_string = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Equipement.csv' AS line
MATCH (door:Door {doorId: line.DoorID})

MERGE (window1:Window {windowId: '1'})
MERGE (desk:Desk {deskId: '1'})

CREATE (window1)-[:ON_THE_RIGHT]->(door)<-[:ON_THE_LEFT]-(desk)

'''
conn.query(query_string, db='graphdb')
#CREATE RELATIONSHIP BETWEEN CHALK,WINDOW2 AND DESK
query_string = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Equipement.csv' AS line
MATCH (desk:Desk {deskId: line.DeskId})

MERGE (chalk:Chalk {chalkId: '1'})
MERGE (window2:Window {windowId: '2'})

CREATE (chalk)-[:ON]->(desk)<-[:ON_THE_LEFT]-(window2)


'''
conn.query(query_string, db='graphdb')
#RELATIONSHIP BETWEEN DESK AND CLASS
query_string = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Equipement.csv' AS line
MATCH (class:Class {classId: line.ClassId})

MERGE (desk:Desk {deskId: '1'})

CREATE (desk)-[:IS_IN]->(class)
'''
conn.query(query_string, db='graphdb')

#CRETA RELATIONSHIP BETWEEN TABLES AND CHAIRS
query_string = '''
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/wassimsmr/PL_AI/main/Equipement.csv' AS line
MATCH (table:Tables)
MATCH (chair:Chairs)
WHERE table.tableId = chair.chairId

MERGE (chair)-[:BEHIND]->(table)
'''
conn.query(query_string, db='graphdb')