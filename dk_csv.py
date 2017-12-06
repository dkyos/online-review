#-*- coding: utf-8 -*-

from dk_header import *
from dk_logger import dk_logger

# singleton logger
logger = dk_logger.get_logger()

def load_csv_to_df(filename):
    df = pd.DataFrame()
    try:
        df = pd.read_csv(filename
            , sep='|'
            , dtype='object'
            , error_bad_lines=False , quoting=csv.QUOTE_NONE
            , encoding='utf-8')
        logger.info("read_csv[%s]: %s" % (filename, df.shape))
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        logger.error("Error[%s]: %s " % (filename, e))

    return df

def save_df_to_csv(df, filename):
    try:
        df.to_csv(filename, sep='|', encoding='utf-8', index=False)
        logger.info("save df(%s) to csv[%s]: %s" % df.shape, filename )
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        logger.error("Error: %s " % e )
    return


