#!/usr/bin/env python
from os import *
import codecs
import getopt
import sys


def main(file, filterfactor, prosup):

	system("python wingkinematics_filter.py %s %s"% (file,filterfactor))
	
	system("python wingkinematics_upsample_v1.0.py %s %s"% (file[:-4]+"_filt.csv",prosup))

	system("python wingkinematics_v5.3.py %s %s"% ((file[:-4]+"_filt_upsampled.csv"),(file[:-4]+"_filt_pron_sup_NEW.csv")))	


######################################################################################################################################################
	


if __name__ == '__main__':

	try:
        	opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
	

    	except getopt.error:
        	sys.stderr.write("%s: %s \nTry `%s --help` for more informatIon\n"
        		% (PROGNAME, e, PROGNAME))
        	sys.exit(1)


    	for o in opts:
        	if o in ('-h', '--help'):
        		usage(error=0)

    	if len(args) != 3:
        	usage()

    	main(args[0],args[1],args[2])

