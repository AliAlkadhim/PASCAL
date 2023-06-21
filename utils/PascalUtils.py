import cx_Oracle
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# USE PYTHON3  !

os.environ['PASCAL']='/home'

############################# Some helper functions ##############
# def printException(exception):
#       error, = exception.args
#   printf("Error code = %s\n",error.code)
#   printf("Error message = %s\n",error.message)

def printf(format,*args):
      sys.stdout.write(format % args)

def show_jupyter_image(image_filename, width=1300, height=300):
    """Show a saved image directly in jupyter. Make sure image_filename is in your IQN_BASE !"""
    display(Image(os.path.join(os.environ['PASCAL'], image_filename), width=width, height=height))

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


  
QUERY2="select * from CMS_HGC_CORE_COND.KINDS_OF_CONDITIONS"

parser=argparse.ArgumentParser(description='query-related arguments')

parser.add_argument('--SensorID', type=str, help='Sensor (scratchpad) ID', required=False,default=None)
parser.add_argument('--outformat', type=str, help='The desired format of the output of the query.', 
                    required=False,default='DF')
parser.add_argument('--maxrows', type=str, help='The desired number of rows to be output from the query.', 
                    required=False,default='all')
parser.add_argument('--query', type=str, help='manual entering of a SQL query at the command line.', 
                    required=False,default=QUERY2)

args = parser.parse_args()

def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_VARCHAR:
        return cursor.var(default_type, size, arraysize=cursor.arraysize,
                          encoding_errors="replace")

# cursor.outputtypehandler = output_type_handler



def execute_query(QUERY, maxrows ='all', outformat='DF', saveformat=None, outstring=None):
    """
    
    Args:
    outformat: the format of the result. DF = pandas.DataFrame(),
    """
    # conn = None
    print('\nExecuting The following SQL Query:\n', QUERY)
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
        df.to_csv(os.path.join(os.environ['PASCAL'], 'query_outputs'
                  '%s.csv' % outstring)
                  )
    # print(df.head())
    return df


def plot_CV(sensor_id):
    # convert SOME_SENSOR_SERIAL_NUMBER in the file to the sensor ID
    cmd = """sed -i "s/'SOME_SENSOR_SERIAL_NUMBER'/'%s'/g" /home/queries/CV_FULL.sql""" % str(sensor_id)
    os.system(cmd)
    CV_QUERY_REP=get_query_from_file(query_file='CV_FULL.sql')
    # remove the last ";" from the sql command in the file to make it executable here
    length=len(CV_QUERY_REP)
    # print(length-1)
    # print(CV_QUERY_REP[:-1])
    CV_QUERY_REP=CV_QUERY_REP[:length-3]
    # print(CV_QUERY_REP[:length-3])
    QUERY_OUT = execute_query(CV_QUERY_REP)
    print(QUERY_OUT.head())
    
    # now convert back to the original SOME_SENSOR_SERIAL_NUMBER
    cmd = """sed -i "s/'%s'/'SOME_SENSOR_SERIAL_NUMBER'/g" /home/queries/CV_FULL.sql""" % str(sensor_id)
    os.system(cmd)
    
    start_time = time.perf_counter()   
    #measure the time for plotting
    max_cells=QUERY_OUT['CELL_NR'].max()
    # serial_number='100383'#aka SCRATCHPAD_ID
    serial_number=sensor_id
    fig,ax=plt.subplots(figsize=(20/3,20/3))
    # colors = mcolors.TABLEAU_COLORS
    # color_list = list(colors.items())
    # color_index = 0
    # cmap = get_cmap(QUERY_OUT.shape[1])
    cmap = get_cmap(255)

    # index = (index + 1) % len(my_list)
    for ind, cell_nr in enumerate(range(1,max_cells)):
        # keep looping back and forth in the colors list
        # color_index = (color_index + 1) % len(colors)
        # color = colors[color_index]
        # print('color index = ', color_index)
        plt.plot(QUERY_OUT['TOT_CURNT_NANOAMP'][QUERY_OUT['CELL_NR']==cell_nr], 
                 QUERY_OUT['ACTUAL_VOLTS'][QUERY_OUT['CELL_NR']==cell_nr], 
                 label = f'cell {cell_nr}',
                alpha=0.4,
                 # color = color_list[color_index][1],
                 # Randomly pick out a color from the cmap
                 color = cmap(ind),
                 linewidth=1.0
                 
                 
                )
        plt.ylabel('Actual Voltage (V)'); plt.xlabel('Total Current (NanoAmp)')
        plt.legend(ncol=5, fontsize=3)
    plt.grid()
    fig.suptitle(serial_number)
    plt.show()
    end_time = time.perf_counter()    
    run_time = end_time - start_time   
    print(f"Finished all plotting in {run_time:.4f} secs")
    # plt.tight_layout()
    
    
if __name__=="__main__":
    HOST='localhost'
    PORT = '10131'
    SERVICE_NAME='int2r_lb.cern.ch'
    PASS=r'HGCAL_Reader_2016'
    USER=r'CMS_HGC_PRTTYPE_HGCAL_READER'
    SensorID=args.SensorID
    outformat=args.outformat
    maxrows=args.maxrows
    
    DSN_TNS = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)
    conn = cx_Oracle.connect(user=USER, password=PASS, dsn=DSN_TNS, 
                       # encoding="UTF-8"
                       ) 
    
    QUERY2="select * from CMS_HGC_CORE_COND.KINDS_OF_CONDITIONS"
    QUERY2_DF = execute_query(QUERY2)
    print(QUERY2_DF.head())