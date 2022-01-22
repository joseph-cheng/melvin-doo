import pymysql
import datetime


class Bill:
	def __init__(self, title, house, votes, date):
		self.title = title
		self.house = house
		self.votes = votes
		self.date = date

class Trade:
	def __init__(self, person, ticker, buy_or_sell, date):
		self.person = person
		self.ticker = ticker
		self.buy_or_sell = buy_or_sell
		self.date = date


def _open_connection():
	conn = pymysql.connect(
		host='localhost',
		user='root',
		password="pass",
		db='melvindoo',
	)

	return conn


def _close_connection(conn):
	conn.close()


def _execute_sql(conn, command):
	cur = conn.cursor()
	cur.execute(command)
	return cur.fetchall()


# Add a new person to the Persons table
def _add_person(conn, name):
	_execute_sql(conn, "INSERT INTO Persons (name) VALUES ('***REMOVED******REMOVED***');".format(name))


# Remove a person from the Persons table
def _remove_person(conn, name):
	_execute_sql(conn, "DELETE FROM Persons WHERE name='***REMOVED******REMOVED***';".format(name))


# Add a new category to the Categories table
def _add_category(conn, category):
	_execute_sql(conn, "INSERT INTO Categories (category) VALUES ('***REMOVED******REMOVED***');".format(category))


# Remove a category from the Categories table
def _remove_category(conn, category):
	_execute_sql(conn, "DELETE FROM Categories WHERE category='***REMOVED******REMOVED***';".format(category))


# Add a new bill to the Bills table
def _add_bill(conn, bill, house):
	_execute_sql(conn, "INSERT INTO Bills (bill, house) VALUES ('***REMOVED***0***REMOVED***', '***REMOVED***1***REMOVED***');".format(bill, house))


# Remove a bill from the Bills table
def _remove_bill(conn, bill):
	_execute_sql(conn, "DELETE FROM Bills WHERE bill='***REMOVED******REMOVED***';".format(bill))


# Add a new company to the Companies table
def _add_company(conn, company):
	_execute_sql(conn, "INSERT INTO Companies (company) VALUES ('***REMOVED******REMOVED***');".format(company))


# Remove a company from the Companies table
def _remove_company(conn, company):
	_execute_sql(conn, "DELETE FROM Companies WHERE company='***REMOVED******REMOVED***';".format(company))


# Add a new bill category pair to the BillCategories table
def _add_bill_category(conn, billID, categoryID):
	_execute_sql(conn, "INSERT INTO BillCategories (bill_ID, category_ID) VALUES (***REMOVED***0***REMOVED***, ***REMOVED***1***REMOVED***);".format(billID, categoryID))


# Remove a bill category pair from the BillCategories table
def _remove_bill_category(conn, billID, categoryID):
	_execute_sql(conn, "DELETE FROM BillCategories WHERE bill_ID = ***REMOVED***0***REMOVED*** AND category_ID = ***REMOVED***1***REMOVED***;".format(billID, categoryID))


# Add a new company category pair to the CompanyCategory table
def _add_company_category(conn, companyID, categoryID):
	_execute_sql(conn, "INSERT INTO CompanyCategories (company_ID, category_ID) VALUES (***REMOVED***0***REMOVED***, ***REMOVED***1***REMOVED***);".format(companyID, categoryID))


# Remove a bill category pair from the BillCategories table
def _remove_company_category(conn, companyID, categoryID):
	_execute_sql(conn, "DELETE FROM CompanyCategories WHERE company_ID = ***REMOVED***0***REMOVED*** AND category_ID = ***REMOVED***1***REMOVED***;".format(companyID, categoryID))


# Add a new trade to the Trades table
def _add_trade(conn, personID, companyID, wasBuy, date):
	_execute_sql(conn, "INSERT INTO Trades (person_ID, company_ID, was_buy, date) VALUES (***REMOVED***0***REMOVED***, ***REMOVED***1***REMOVED***, ***REMOVED***2***REMOVED***, '***REMOVED***3***REMOVED***');".format(personID, companyID, 1 if wasBuy else 0, date))


# Remove a trade from the Trades table
def _remove_trade(conn, personID, companyID, wasBuy, date):
	_execute_sql(conn, "DELETE FROM Trades WHERE person_ID = ***REMOVED***0***REMOVED*** AND company_ID = ***REMOVED***1***REMOVED*** AND was_buy = ***REMOVED***2***REMOVED*** AND date = '***REMOVED***3***REMOVED***';".format(personID, companyID, 1 if wasBuy else 0, date))


# Add a new vote to the Votes table
def _add_vote(conn, personID, billID, votedFor, date):
	_execute_sql(conn, "INSERT INTO Votes (person_ID, bill_ID, voted_for, date) VALUES (***REMOVED***0***REMOVED***, ***REMOVED***1***REMOVED***, ***REMOVED***2***REMOVED***, '***REMOVED***3***REMOVED***');".format(personID, billID, 1 if votedFor else 0, date))


# Remove a vote from the Votes table
def _remove_vote(conn, personID, billID, votedFor, date):
	_execute_sql(conn, "DELETE FROM Votes WHERE person_ID = ***REMOVED***0***REMOVED*** AND bill_ID = ***REMOVED***1***REMOVED*** AND voted_for = ***REMOVED***2***REMOVED*** AND date = '***REMOVED***3***REMOVED***';".format(personID, billID, 1 if votedFor else 0, date))


# Select all from a table
def _select_all(conn, tableName):
	return _execute_sql(conn, "SELECT * FROM ***REMOVED******REMOVED***;".format(tableName))


def _get_query(conn, query):
	return _execute_sql(conn, query)


def _get_id(conn, table, column, value):
	res = _get_query(conn, "SELECT ID FROM ***REMOVED***0***REMOVED*** WHERE ***REMOVED***1***REMOVED*** = '***REMOVED***2***REMOVED***';".format(table, column, value))
	if len(res) == 0:
		return None
	return int(res[0][0])


def process_vote(conn, bill):
	# Extract variables from bill
	title = bill.title
	house = bill.house
	categories = ["defence", "housing"] #bill.categories
	votes = bill.votes
	date = datetime.date.today()

	# Add new bill
	_add_bill(conn, title, house)
	billID = _get_id(conn, "Bills", "bill", title)

	# Categorise the bill in the BillCategories table
	for category in categories:
		categoryID = _get_id(conn, "Categories", "category", category)
		if categoryID is None:
			# Have found a new category so add it to Categories
			_add_category(conn, category)
			categoryID = _get_id(conn, "Categories", "category", category)
		_add_bill_category(conn, billID, categoryID)

	# Create a vote entry for each person voting on this bill
	for person, vote in votes:
		personID = _get_id(conn, "Persons", "name", person)
		if personID is None:
			_add_person(conn, person)
			personID = _get_id(conn, "Persons", "name", person)
		voted_for = vote == 1
		_add_vote(conn, personID, billID, voted_for, date)


def process_trade(conn, trade):
	# Extract variables from trade
	person = trade.person
	ticker = trade.ticker
	buy_or_sell = trade.buy_or_sell == "buy"
	categories = _get_company_categories(ticker)
	date = trade.date # datetime.date.today()

	# Get the person ID (or add to Persons if a new person)
	personID = _get_id(conn, "Persons", "name", person)
	if personID is None:
		_add_person(conn, person)
		personID = _get_id(conn, "Persons", "name", person)

	# Get the ticker ID (or add to Companies if a new ticker)
	tickerID = _get_id(conn, "Companies", "company", ticker)
	if tickerID is None:
		_add_company(conn, ticker)
		tickerID = _get_id(conn, "Companies", "company", ticker)

	# Categorise the ticker in the CompanyCategories table
	for category in categories:
		categoryID = _get_id(conn, "Categories", "category", category)
		if categoryID is None:
			# Have found a new category so add it to Categories
			_add_category(conn, category)
			categoryID = _get_id(conn, "Categories", "category", category)
		if len(_get_query(conn, "SELECT * FROM CompanyCategories WHERE company_ID = ***REMOVED***0***REMOVED*** AND category_ID = ***REMOVED***1***REMOVED***;".format(tickerID, categoryID))) == 0:
			_add_company_category(conn, tickerID, categoryID)

	_add_trade(conn, personID, tickerID, buy_or_sell, date)


def _get_company_categories(company):
	return ["defence", "healthcare"]


def get_votes_influenced_by_trades(conn, person, time_range=5):

	conflicts = []

	personID = _get_id(conn, "Persons", "name", person)

	query = "SELECT *, DATEDIFF(Votes.date, Trades.date) AS difference FROM Votes"
	query += " INNER JOIN BillCategories AS bc ON bc.bill_ID = Votes.bill_ID"
	query += " INNER JOIN Categories AS cat ON cat.ID = bc.category_ID"
	query += " INNER JOIN Trades ON Trades.person_ID = Votes.person_ID"
	query += " INNER JOIN CompanyCategories AS cc ON (cc.company_ID = Trades.company_ID AND cc.category_ID = cat.ID)"
	query += " WHERE (Votes.person_ID = '***REMOVED******REMOVED***');".format(personID)

	res = _get_query(conn, query)
	'''print("")
	print("RES:")
	print(res)
	print("")'''

	for result in res: # 0=vote id, 1=person id, 2=bill id, 3=was for, 4=bill date, 5=bill category id, 6=bill id, 7=category id, 8=category id, 9=category, 10=trade id, 11=person id, 12=company id
		# 13=was_buy, 14=trade date, 15=company category id, 16=company id, 17=category id, 18=date diff

		if result[18] > time_range:
			print("OUT OF RANGE")
			continue

		bill_id = result[2]
		bill_voted_for = result[3]
		bill_date = result[4]

		trade_company_id = result[12]
		trade_was_buy = result[13]
		trade_date = result[14]

		shared_category = result[9]

		bill_name = _get_query(conn, "SELECT bill FROM bills WHERE id = ***REMOVED******REMOVED***;".format(bill_id))[0][0]
		trade_company = _get_query(conn, "SELECT company FROM companies WHERE id = ***REMOVED******REMOVED***;".format(trade_company_id))[0][0]

		print("Result: bill - ***REMOVED***0***REMOVED***, voted for - ***REMOVED***1***REMOVED***, date - ***REMOVED***2***REMOVED***, trade name - ***REMOVED***3***REMOVED***, type - ***REMOVED***4***REMOVED***, date - ***REMOVED***5***REMOVED***, category - ***REMOVED***6***REMOVED***".format(bill_name, bill_voted_for, bill_date, trade_company, trade_was_buy, trade_date, shared_category))
		conflicts.append((bill_name, bill_voted_for, bill_date, trade_company, trade_was_buy, trade_date, shared_category))

	'''tables = _get_query(conn, "SHOW TABLES;")
	print(tables)
	for table in tables:
		print("Table: " + str(table[0]))
		print(_select_all(conn, table[0]))'''

	return conflicts


if __name__ == "__main__":
	conn = _open_connection()

	process_vote(conn, Bill("Bill of Rights", "house", [("Will", 1),("Aga", 0),("Joe", 0),("Maxim", 1)], datetime.date.today()))
	process_trade(conn, Trade("Will", "TSL", "buy", datetime.date.today()))
	conflicts = get_votes_influenced_by_trades(conn, "Will")
	print("Conflicts: ***REMOVED******REMOVED***".format(conflicts))

	_close_connection(conn)


