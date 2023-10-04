import cx_Oracle
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse
import os
import IPython
from IPython.display import Image, display
import time
# USE PYTHON3  !

os.environ['PASCAL']='/home'
PASCAL=os.environ['PASCAL']
OUTPUT_DIR=os.path.join(PASCAL,'outputs')
QUERY_DIR=os.path.join(PASCAL,'queries')
LOG_DIR=os.path.join(PASCAL,'logs')

############################# Some helper functions ##############
# def printException(exception):
#       error, = exception.args
#   printf("Error code = %s\n",error.code)
#   printf("Error message = %s\n",error.message)

def printf(format,*args):
      sys.stdout.write(format % args)

def show_jupyter_image(image_filename, width=1300, height=300):
    """Show a saved image directly in jupyter. Make sure image_filename is in your IQN_BASE !"""
    display(Image(os.path.join(os.environ['PASCAL'], 'images', image_filename), width=width, height=height))

def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow



############################ Some decorators ############################
def SourcePASCAL(func):
    def _func(*args):
        import os
        from common.utility.source import source

        env = {}
        env.update(os.environ)
        env.update(source(os.environ["PASCAL"]))
        func(*args, env=env)

    return _func

def debug(func):
    """Print the function signature and return value"""
    import functools

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        values = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {values!r}")
        return values

    return wrapper_debug

def make_interactive(func):
    """make the plot interactive"""
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        plt.ion()
        output = func(*args, **kwargs)
        plt.ioff()
        return output

    return wrapper

def timer(func):
    """Print the runtime of the decorated function"""
    import functools
    import time
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"\nFINISHED {func.__name__!r} in {run_time:.4f} SECS")
        return value
    return wrapper_timer

# from IPython.core.magic import register_cell_magic

# @register_cell_magic
def write_and_run(line, cell):
    """write the current cell to a file (or append it with -a argument) as well as execute it
    use with %%write_and_run at the top of a given cell"""
    argz = line.split()
    file = argz[-1]
    mode = "w"
    if len(argz) == 2 and argz[0] == "-a":
        mode = "a"
    with open(file, mode) as f:
        f.write(cell)
    # get_ipython().run_cell(cell)
############################  ############################

HOST='localhost'
PORT = '10131'
SERVICE_NAME='int2r_lb.cern.ch'
PASS=r'HGCAL_Reader_2016'
USER=r'CMS_HGC_PRTTYPE_HGCAL_READER'

DSN_TNS = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)

def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_VARCHAR:
        return cursor.var(default_type, size, arraysize=cursor.arraysize,
                          encoding_errors="replace")

# cursor.outputtypehandler = output_type_handler

conn = cx_Oracle.connect(user=USER, password=PASS, dsn=DSN_TNS, 
                       # encoding="UTF-8"
                       ) 
def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow

@timer
def execute_query(QUERY, maxrows ='all', outformat='DF', saveformat=None, outstring=None):
    """
    
    Args:
    outformat: the format of the result. DF = pandas.DataFrame(),
    """
    # conn = None
    try:
    # if you want a new connection and close it at the end, uncomment below
      conn = cx_Oracle.connect(user=USER, password=PASS, dsn=DSN_TNS, 
                               # encoding="UTF-8"
                               ) 


      cursor = conn.cursor()

    except Exception as err:
      print('Connection error')
      print(err)
    finally:
      if conn:
            if maxrows=='all':
            # execute
                cursor.execute(QUERY)
            # rows = cursor.execute(QUERY2)
            # cursor.execute(QUERY_TIME_3)
            # conn.commit()
            else:
                cursor.execute(QUERY,offset=0, maxnumrows=maxrows)
            
            # try:
              # rows=cursor.fetall()
            # except Exception as err:
              # print(err)
            columnNames = [d[0] for d in cursor.description]
            print('\nCOLUMN NAMES:\n', columnNames)
            # for row in rows:
                  # print(list(row))
            #return result as a dictionary
            result = [dict(zip(columnNames, row)) for row in cursor.fetchall()]
            # result=None
            cursor.close()
            conn.close()
    
    if outformat=='DF':
        df =pd.DataFrame(result)
    
    
    
    if saveformat=='CSV':
        df.to_csv(f'{outstring}.csv')
    # print(df.head())
    return df

def get_query_from_file(query_file):
    query_file_path = os.path.join(QUERY_DIR,query_file)
    query_f = open(query_file_path)
    QUERY = query_f.read()
    # print(QUERY)
    query_f.close()

    return QUERY