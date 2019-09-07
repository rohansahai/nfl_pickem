import sqlalchemy as alch


_engines = {}


class db_conn():
    """
    Creates new database connection context using cached sqlalchemy engines,
    each of which manages a connection pool.

    Usage:

    with db_conn(connection_string) as conn:
        curs = conn.execute(sql)
        ...

    """

    def __init__(self, conn_str):
        """
        Parameters
        ----------
        RFC-1738 database connection URL
        """
        self.conn_str = conn_str

    def __enter__(self):
        """
        Open connection to a database (acquire from connection pool)

        Returns
        -------
        SqlAlchemy Connection object
        """

        if self.conn_str not in _engines:
            engine = alch.create_engine(self.conn_str)
            _engines[self.conn_str] = engine

        self.conn_str = self.conn_str

        return _engines[self.conn_str].connect()

    def __exit__(self, type, value, traceback):
        """
        Close connection to db (return to connection pool)
        """
        try:
            _engines[self.conn_str].close()
        except:
            pass


def update(conn, sql):
    with db_conn(conn) as conn:
        conn.execute(sql)


def get_ff_url(current_week):

    return 'https://www.fleaflicker.com/nfl/scores?week={}'.format(current_week)


def get_vi_url(week):

    return "http://www.vegasinsider.com/nfl/matchups/matchups.cfm/week/{}/season/2019".format(week)


def get_gmail_creds():

    return 'shaun.chaudhary@gmail.com', 'bjfwispetfyhzkxd'


def get_local_str():

    prod_str = 'postgresql+psycopg2://dtaxgwznvvlhde:6tiVAc1zqt3WKf4pfty52ti0Tw@ec2-54-243-217-22.compute-1.amazonaws.com:5432/deij2vlu5g0eh8'

    return prod_str