#search.py
import sqlite3

def search_plant():
	with sqlite3.connect('bazadedate.db') as db:
		cursor=db.cursor()
		sql="SELECT Engleza  FROM INFORMATION"
		cursor.execute(sql)
		product=cursor.fetchall()
		db.commit()
		return product


def retrease_data():
	search_plant()
	liste=[]
	numeleLor=""

	for i in search_plant():
		liste.append(i)

	for j in liste:
		a="".join(j)
		numeleLor +=a + "," 
	
	lista_finala =numeleLor.split(",")
	
	return lista_finala[0:-1]

def make_a_search(text_to_search):
	with sqlite3.connect('bazadedate.db') as db:
		cursor=db.cursor()
		data=(text_to_search,)
		sql="SELECT Spaniola,Audio  FROM INFORMATION where Engleza=?"
		cursor.execute(sql,data)
		product=cursor.fetchall()
		db.commit()
		return product
