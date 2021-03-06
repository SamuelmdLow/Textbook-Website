import sqlite3
import pathlib

DATABASE_FILE   =   "database.db"

FIRST_RUN   =   True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN   =   False

CONNECTION  =   sqlite3.connect(DATABASE_FILE, check_same_thread=False)
CURSOR      =   CONNECTION.cursor()

def createDatabase():
    global CURSOR, CONNECTION

    CURSOR.execute('''
        CREATE TABLE
            textbooks (
                id INTEGER PRIMARY KEY,
                name TEXT
            )           
    ;''')

    CURSOR.execute('''
        CREATE TABLE
            sections (
                textbookId INTEGER,
                sectionNum INTEGER,
                content TEXT
            )           
    ;''')

    CURSOR.execute('''
        CREATE TABLE
            tags (
                textbookId INTEGER,
                tag TEXT
            )           
    ;''')

    CONNECTION.commit()

def addTextbook(name):

    CURSOR.execute('''
        INSERT INTO
            textbooks(
                name
            )
        VALUES(
            ?
        )           
    ;''',[name]).fetchone()

    CONNECTION.commit()

    index = CURSOR.execute('''
        SELECT
            id
        FROM 
            textbooks
        ORDER BY
            id DESC
    ;''').fetchone()[0]

    return index

def getInfo(textbookId):

    global CURSOR, CONNECTION

    textbookId = int(textbookId)

    name = CURSOR.execute('''
        SELECT
            name
        FROM 
            textbooks
        WHERE
            id = ?
    ;''',[textbookId]).fetchone()[0]

    data = [name]

    content = CURSOR.execute('''
        SELECT
            content
        FROM 
            sections
        WHERE
            textbookId = ?
        ORDER BY
            sectionNum ASC
    ;''',[textbookId]).fetchall()
    print(content)
    content = [i[0].split(",") for i in content]
    print(content)
    data.append(content)

    print(data)
    return data

def getUsersBooks():
    global CURSOR
    books = CURSOR.execute('''
        SELECT
            *
        FROM
            textbooks
        ORDER BY
            id DESC    
    ;''').fetchall()
    return books

def update(id, contents):
    global CURSOR, CONNECTION

    print("thing2")
    print(contents)

    contents = contents.split("|")
    if len(contents) > 0:
        contents.pop(0)
    print(contents)

    CURSOR.execute('''
        DELETE FROM
            sections
        WHERE
            textbookId = ?
    ;''',[id])

    for section in range(len(contents)):
        print(contents[section])
        CURSOR.execute('''
              INSERT INTO
                  sections(
                     textbookId,
                     sectionNum,
                     content
                  )
              VALUES(
                  ?, ?, ?
              )
        ;''', [id, section, contents[section]])
    CONNECTION.commit()

if FIRST_RUN == True:
    createDatabase()