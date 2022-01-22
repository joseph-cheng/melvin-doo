import pymysql
import datetime


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
	_execute_sql(conn, "INSERT INTO Persons (name) VALUES ('{}');".format(name))


# Remove a person from the Persons table
def _remove_person(conn, name):
	_execute_sql(conn, "DELETE FROM Persons WHERE name='{}';".format(name))


# Add a new category to the Categories table
def _add_category(conn, category):
	_execute_sql(conn, "INSERT INTO Categories (category) VALUES ('{}');".format(category))


# Remove a category from the Categories table
def _remove_category(conn, category):
	_execute_sql(conn, "DELETE FROM Categories WHERE category='{}';".format(category))


# Add a new bill to the Bills table
def _add_bill(conn, bill, house):
	_execute_sql(conn, "INSERT INTO Bills (bill, house) VALUES ('{0}', '{1}');".format(bill, house))


# Remove a bill from the Bills table
def _remove_bill(conn, bill):
	_execute_sql(conn, "DELETE FROM Bills WHERE bill='{}';".format(bill))


# Add a new company to the Companies table
def _add_company(conn, company):
	_execute_sql(conn, "INSERT INTO Companies (company) VALUES ('{}');".format(company))


# Remove a company from the Companies table
def _remove_company(conn, company):
	_execute_sql(conn, "DELETE FROM Companies WHERE company='{}';".format(company))


# Add a new bill category pair to the BillCategories table
def _add_bill_category(conn, billID, categoryID):
	_execute_sql(conn, "INSERT INTO BillCategories (bill_ID, category_ID) VALUES ({0}, {1});".format(billID, categoryID))


# Remove a bill category pair from the BillCategories table
def _remove_bill_category(conn, billID, categoryID):
	_execute_sql(conn, "DELETE FROM BillCategories WHERE bill_ID = {0} AND category_ID = {1};".format(billID, categoryID))


# Add a new company category pair to the CompanyCategory table
def _add_company_category(conn, companyID, categoryID):
	_execute_sql(conn, "INSERT INTO CompanyCategories (company_ID, category_ID) VALUES ({0}, {1});".format(companyID, categoryID))


# Remove a bill category pair from the BillCategories table
def _remove_company_category(conn, companyID, categoryID):
	_execute_sql(conn, "DELETE FROM CompanyCategories WHERE company_ID = {0} AND category_ID = {1};".format(companyID, categoryID))


# Add a new trade to the Trades table
def _add_trade(conn, personID, companyID, wasBuy, date):
	_execute_sql(conn, "INSERT INTO Trades (person_ID, company_ID, was_buy, date) VALUES ({0}, {1}, {2}, {3});".format(personID, companyID, 1 if wasBuy else 0, date))


# Remove a trade from the Trades table
def _remove_trade(conn, personID, companyID, wasBuy, date):
	_execute_sql(conn, "DELETE FROM Trades WHERE person_ID = {0} AND company_ID = {1} AND was_buy = {2} AND date = {3};".format(personID, companyID, 1 if wasBuy else 0, date))


# Add a new vote to the Votes table
def _add_vote(conn, personID, billID, votedFor, date):
	_execute_sql(conn, "INSERT INTO Votes (person_ID, bill_ID, voted_for, date) VALUES ({0}, {1}, {2}, {3});".format(personID, billID, 1 if votedFor else 0, date))


# Remove a vote from the Votes table
def _remove_vote(conn, personID, billID, votedFor, date):
	_execute_sql(conn, "DELETE FROM Votes WHERE person_ID = {0} AND bill_ID = {1} AND voted_for = {2} AND date = {3};".format(personID, billID, 1 if votedFor else 0, date))


# Select all from a table
def _select_all(conn, tableName):
	print(_execute_sql(conn, "SELECT * FROM {};".format(tableName)))


def _get_query(conn, query):
	return _execute_sql(conn, query)


def _get_id(conn, table, column, value):
	res = _get_query(conn, "SELECT ID FROM {0} WHERE {1} = '{2}';".format(table, column, value))
	if len(res) == 0:
		return None
	return int(res[0][0])


def process_vote(bill):
	conn = _open_connection()

	# Extract variables from bill
	title = bill.title
	house = bill.house
	categories = [] #bill.categories
	votes = bill.votes

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
		date = datetime.date.today()
		_add_vote(conn, personID, billID, voted_for, date)

	_close_connection(conn)


def process_trade(trade):
	conn = _open_connection()

	# Extract variables from trade
	person = trade.person
	ticker = trade.ticker
	buy_or_sell = trade.buy_or_sell == "buy"
	categories = _get_company_categories(ticker)
	date = datetime.date.today()

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
		if len(_get_query(conn, "SELECT * FROM CompanyCategories WHERE company_ID = {0} AND category_ID = {1};".format(tickerID, categoryID))) == 0:
			_add_company_category(conn, tickerID, categoryID)

	_add_trade(conn, personID, tickerID, buy_or_sell, date)

	_close_connection(conn)


def _get_company_categories(company):
	return []


def get_votes_influenced_by_trades(person, time_range=5):
	conn = _open_connection()

	votes = []
	trade = None

	

	_close_connection(conn)

	return votes, trade


if __name__ == "__main__":
	conn = _open_connection()
	_close_connection(conn)