#!/usr/bin/python
import argparse
import json
import subprocess
import os

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
			wait(10)
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
