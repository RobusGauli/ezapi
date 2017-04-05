__author__ = 'robusgauli@gmail.com'

from ezapi.pqb.exceptions import BadQueryException


class Column(object):
    def __init__(self, name):
        self.name = name
    
    def get_string(self):
        if self.name:
            return str(self.name)
        else:
            raise ValueError('Can\'t convert to string')
            return

    def __repr__(self):
        return '<Column : {}>'.format(self.name)
    
    def __str__(self):
        return str(self.name)
    

class QueryBuilder(object):

    def __init__(self):
        self.SELECT  = 'SELECT '
        self.FROM = 'FROM '
        self.WHERE = ''
        self.INSERT = 'INSERT INTO '
        self.VALUES = 'VALUES'
        self.select_query = False
        self.update_query = False
        self.insert_query = False
    
    def select(self, *cols):
        '''This method will chain the columns together'''

        if self.update_query or self.select_query:
            raise BadQuery('Bad Query chaining')

        self.SELECT  += ', '.join(col.get_string() for col in cols)
        #now update the select_query to true
        self.select_query = True
        return self
    
    def _from(self, table):
        self.FROM += table.__tablename__
        return self
    
    def where(self, col, val):
        val = "'{0}'".format(val) if isinstance(val, str) else str(val)
        self.WHERE += ('WHERE '+ col.get_string() + ' = ' + val)
        return self
    
    def _and(self, col, val):
        val = "'{0}'".format(val) if isinstance(val, str) else str(val)
        self.WHERE += (' and ' + col.get_string()) + ' = ' + val
        return self
    
    def _get_select_query(self):
        return self.SELECT + ' ' + self.FROM + ' '+ self.WHERE
    
    def insert(self, table, *cols):
        if self.select_query or self.insert_query:
            raise BadQuery('Bad Query Chaining')
        self.INSERT += table.__tablename__
        self.INSERT += ' ({0})'.format(', '.join(str(col) for col in cols))
        self.insert_query = True
        return self

    
    
    def values(self, *vals):

        formatted_vals = ("'{0}'".format(str(val)) if isinstance(val, str) else str(val) for val in vals)
        
        self.VALUES += ' ({0}) '.format(',  '.join(val for val in formatted_vals))

        return self
         
    
    def _get_insert_query(self):
        return self.INSERT + ' ' + self.VALUES

    def __call__(self):
        if self.select_query:
            return self._get_select_query()
        elif self.insert_query:
            return self._get_insert_query()
    