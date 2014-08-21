__author__ = 'bill'
import re, os, time
import logging
logger = logging.getLogger(__name__)


def choose_league_directory(listings):
    r = re.compile(r'league_(\d+)')
    l = [int(re.search(r, o).group(1)) for o in listings if re.search(r, o)]
    logger.debug("league directory is %s" % str(l))
    if len(l) == 0:
        logger.debug("no leagues matched")
        return None
    l.sort(reverse=True)
    logger.info("choose_directory(): %s" % (str(l)))
    n = str(l[0])
    n = n.zfill(3)
    for listing in listings:
        search = 'league_' + n
        logger.debug('choose_directory(): trying to match on ' + search)
        if re.search(search, listing):
            logger.debug("choose_directory(): found match on %s " % listing)
            return listing
    return None

def create_league_directory(number):
    logger.debug('create_league_directory(): begin .. %d ' % number)
    datestr = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    logger.debug('create_league_directory(): date str is  ' + datestr)
    numberstr = str(number).zfill(3)
    name = 'league_' + numberstr + '_' + datestr
    leagues_dir = os.path.join(os.getcwd(), 'leagues')
    if not os.path.exists(leagues_dir):
        os.mkdir(leagues_dir)
    league_path = os.path.join(leagues_dir, name)
    logger.debug('create_league_directory(): creating league dir %s ' % league_path)
    if not os.path.isdir(league_path):
        if os.path.exists(league_path):
            raise Exception("league path %s already exists " % league_path)
        os.mkdir(league_path)
    return league_path

