import pymysql
import datetime
import companies_scraper

'''
Useful methods:
	- _open_connection() - open up a connection to the database, returns the connection
	- _close_connection(conn) - saves and closes the connection to the database
	- get_votes_influenced_by_trades(person, time_range=5) - return a list of conflicts between trades and votes by a given person
	- get_votes_influenced_by_trades_filtered_by_category(person, category, time_range=5) - return a list of conflicts between trades and votes by a given person for a given category
'''
# Useful methods:



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


def open_connection():
	conn = pymysql.connect(
		host='localhost',
		user='user',
		password="pass",
		db='melvindoo',
	)

	return conn


def close_connection(conn):
	conn.commit()
	conn.close()


def _execute_sql(conn, command):
	cur = conn.cursor()
	cur.execute(command)
	return cur.fetchall()


# Add a new person to the Persons table
def _add_person(conn, name):
	_execute_sql(conn, "INSERT INTO persons (name) VALUES ('{}');".format(name))


# Remove a person from the Persons table
def _remove_person(conn, name):
	_execute_sql(conn, "DELETE FROM persons WHERE name='{}';".format(name))


# Add a new category to the Categories table
def _add_category(conn, category):
	_execute_sql(conn, "INSERT INTO categories (category) VALUES ('{}');".format(category))


# Remove a category from the Categories table
def _remove_category(conn, category):
	_execute_sql(conn, "DELETE FROM categories WHERE category='{}';".format(category))


# Add a new bill to the Bills table
def _add_bill(conn, bill, house):
	_execute_sql(conn, "INSERT INTO bills (bill, house) VALUES ('{0}', '{1}');".format(bill, house))


# Remove a bill from the Bills table
def _remove_bill(conn, bill):
	_execute_sql(conn, "DELETE FROM bills WHERE bill='{}';".format(bill))


# Add a new company to the Companies table
def _add_company(conn, company):
	_execute_sql(conn, "INSERT INTO companies (company) VALUES ('{}');".format(company))


# Remove a company from the Companies table
def _remove_company(conn, company):
	_execute_sql(conn, "DELETE FROM companies WHERE company='{}';".format(company))


# Add a new bill category pair to the BillCategories table
def _add_bill_category(conn, billID, categoryID):
	_execute_sql(conn, "INSERT INTO billcategories (bill_ID, category_ID) VALUES ({0}, {1});".format(billID, categoryID))


# Remove a bill category pair from the BillCategories table
def _remove_bill_category(conn, billID, categoryID):
	_execute_sql(conn, "DELETE FROM billcategories WHERE bill_ID = {0} AND category_ID = {1};".format(billID, categoryID))


# Add a new company category pair to the CompanyCategory table
def _add_company_category(conn, companyID, categoryID):
	_execute_sql(conn, "INSERT INTO companycategories (company_ID, category_ID) VALUES ({0}, {1});".format(companyID, categoryID))


# Remove a bill category pair from the BillCategories table
def _remove_company_category(conn, companyID, categoryID):
	_execute_sql(conn, "DELETE FROM companycategories WHERE company_ID = {0} AND category_ID = {1};".format(companyID, categoryID))


# Add a new trade to the Trades table
def _add_trade(conn, personID, companyID, wasBuy, date):
	_execute_sql(conn, "INSERT INTO trades (person_ID, company_ID, was_buy, date) VALUES ({0}, {1}, '{2}', STR_TO_DATE('{3}', \"%Y-%m-%d\"));".format(personID, companyID, "buy" if wasBuy else "sell", date))


# Remove a trade from the Trades table
def _remove_trade(conn, personID, companyID, wasBuy, date):
	_execute_sql(conn, "DELETE FROM trades WHERE person_ID = {0} AND company_ID = {1} AND was_buy = {2} AND date = {3};".format(personID, companyID, 1 if wasBuy else 0, date))


# Add a new vote to the Votes table
def _add_vote(conn, personID, billID, votedFor, date):
	_execute_sql(conn, "INSERT INTO votes (person_ID, bill_ID, voted_for, date) VALUES ({0}, {1}, {2}, {3});".format(personID, billID, "for" if votedFor else "against", date))


# Remove a vote from the Votes table
def _remove_vote(conn, personID, billID, votedFor, date):
	_execute_sql(conn, "DELETE FROM votes WHERE person_ID = {0} AND bill_ID = {1} AND voted_for = {2} AND date = {3};".format(personID, billID, 1 if votedFor else 0, date))


# Select all from a table
def _select_all(conn, tableName):
	return _execute_sql(conn, "SELECT * FROM {};".format(tableName))


def _get_query(conn, query):
	return _execute_sql(conn, query)


def _get_id(conn, table, column, value):
	res = _get_query(conn, "SELECT ID FROM {0} WHERE {1} = '{2}';".format(table, column, value))
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
	billID = _get_id(conn, "bills", "bill", title)

	# Categorise the bill in the BillCategories table
	for category in categories:
		categoryID = _get_id(conn, "categories", "category", category)
		if categoryID is None:
			# Have found a new category so add it to Categories
			_add_category(conn, category)
			categoryID = _get_id(conn, "categories", "category", category)
		_add_bill_category(conn, billID, categoryID)

	# Create a vote entry for each person voting on this bill
	for person, vote in votes:
		personID = _get_id(conn, "persons", "name", person)
		if personID is None:
			_add_person(conn, person)
			personID = _get_id(conn, "persons", "name", person)
		voted_for = vote == 1
		_add_vote(conn, personID, billID, voted_for, date)


def process_trade(conn, trade):
	# Extract variables from trade
	person = trade.person
	ticker = trade.ticker
	buy_or_sell = True if trade.buy_or_sell == "buy" else False
	date = trade.date

	# Get the person ID (or add to Persons if a new person)
	personID = _get_id(conn, "persons", "name", person)
	if personID is None:
		_add_person(conn, person)
		personID = _get_id(conn, "persons", "name", person)

	# Get the ticker ID (or add to Companies if a new ticker)
	tickerID = _get_id(conn, "companies", "company", ticker)
	if tickerID is None:
		_add_company(conn, ticker)
		tickerID = _get_id(conn, "companies", "company", ticker)

	_add_trade(conn, personID, tickerID, buy_or_sell, date)


def fill_tickers_and_categories(conn):
	pairs = companies_scraper.get_ticker_categories()

	for company, categories in pairs:
		# Get the ticker ID (or add to Companies if a new ticker)
		ticker_id = _get_id(conn, "companies", "company", company)
		if ticker_id is None:
			_add_company(conn, company)
			ticker_id = _get_id(conn, "companies", "company", company)

		for category in categories:

			category_id = _get_id(conn, "categories", "category", category)
			if category_id is None:
				# Have found a new category so add it to Categories
				_add_category(conn, category)
				category_id = _get_id(conn, "categories", "category", category)

			_add_company_category(conn, ticker_id, category_id)


def get_votes_influenced_by_trades(person, time_range=5):
	conn = open_connection()

	person_id = _get_id(conn, "Persons", "name", person)

	query = _get_initial_query_auxiliary()
	query += " WHERE (Votes.person_ID = '{}');".format(person_id)

	return _get_votes_auxiliary(conn, query, time_range)


def get_votes_influenced_by_trades_filtered_by_category(person, category, time_range=5):
	conn = open_connection()

	person_id = _get_id(conn, "Persons", "name", person)
	category_id = _get_id(conn, "Categories", "category", category)

	query = _get_initial_query_auxiliary()
	query += " WHERE (Votes.person_ID = '{0}' AND cat.ID = {1});".format(person_id, category_id)

	return _get_votes_auxiliary(conn, query, time_range)


def _get_initial_query_auxiliary():
	query = "SELECT *, DATEDIFF(Votes.date, Trades.date) AS difference FROM Votes"
	query += " INNER JOIN BillCategories AS bc ON bc.bill_ID = Votes.bill_ID"
	query += " INNER JOIN Categories AS cat ON cat.ID = bc.category_ID"
	query += " INNER JOIN Trades ON Trades.person_ID = Votes.person_ID"
	query += " INNER JOIN CompanyCategories AS cc ON (cc.company_ID = Trades.company_ID AND cc.category_ID = cat.ID)"
	return query


def _get_votes_auxiliary(conn, query, time_range):
	conflicts = []

	res = _get_query(conn, query)

	for result in res:  # 0=vote id, 1=person id, 2=bill id, 3=was for, 4=bill date, 5=bill category id, 6=bill id, 7=category id, 8=category id, 9=category, 10=trade id, 11=person id, 12=company id
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

		bill_name = _get_query(conn, "SELECT bill FROM bills WHERE id = {};".format(bill_id))[0][0]
		trade_company = _get_query(conn, "SELECT company FROM companies WHERE id = {};".format(trade_company_id))[0][0]

		# print("Result: bill - {0}, voted for - {1}, date - {2}, trade name - {3}, type - {4}, date - {5}, category - {6}".format(bill_name, bill_voted_for, bill_date, trade_company, trade_was_buy, trade_date, shared_category))
		conflicts.append(
			(bill_name, bill_voted_for, bill_date, trade_company, trade_was_buy, trade_date, shared_category))

	close_connection(conn)

	return conflicts


if __name__ == "__main__":
	'''conn = _open_connection()

	process_vote(conn, Bill("Bill of Rights", "house", [("Will", 1),("Aga", 0),("Joe", 0),("Maxim", 1)], datetime.date.today()))
	process_trade(conn, Trade("Will", "TSL", "buy", datetime.date.today()))
	conflicts = get_votes_influenced_by_trades(conn, "Will")
	print("Conflicts: {}".format(conflicts))

	_close_connection(conn)'''
	pass