#!/usr/bin/python
import argparse
import json
import subprocess
import os
import time
import sys



def progressbar():
	toolbar_width=100
	# setup toolbar
	sys.stdout.write("%s" % (" " * toolbar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * toolbar_width) # return to start of line, after	'['

	for i in xrange(toolbar_width):
			time.sleep(1) # do real work here
			# update the bar
			sys.stdout.write("-")
			sys.stdout.flush()

def main(afi):

	d_afi= None
	with open(afi,'r') as f:
		d_afi = json.load(f)

	afi_id = d_afi['FpgaImageId']

	arg_status = list()
	arg_status.append('aws')
	arg_status.append('ec2')
	arg_status.append('describe-fpga-images')
	arg_status.append('--fpga-image-ids')
	arg_status.append(afi_id)
	while True:
		p = subprocess.Popen(arg_status, stdout=subprocess.PIPE)
		p.wait()
		out, err = p.communicate()
		j_st = json.loads(out)
		code = j_st["FpgaImages"][0]["State"]["Code"]
		if code =='pending':
			progressbar()
		elif code =='available':
			print("Image available online")
			print("Finished")
			break
		else:
			print("Unknow code, please fix it.")
			break





if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Check the status of the image on AWS")
	parser.add_argument('--afi', help="AFI filename")
	args = parser.parse_args()
	if args.afi==None:
		parser.print_help()
	else:
		main(args.afi)
