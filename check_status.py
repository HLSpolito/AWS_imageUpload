#!/usr/bin/python
import argparse
import json
import subprocess
import os

def main(afi, kn):

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
	p = subprocess.Popen(arg_status, stdout=subprocess.PIPE)
	out, err = p.communicate()

	j_st = json.loads(out)
	code = j_st["FpgaImages"][0]["State"]["Code"]
	if code =='pending':
		wait(10)
	elif code =='available':
		print("Image available online")
		print("Finished")
		return





if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Audio Transcription")
	parser.add_argument('--afi', help="AFI file")
#	parser.add_argument('--k_n', help="Kernel name")
	args = parser.parse_args()
	if args.afi==None:# or args.k_n==None:
		parser.print_help()
	else:
		main(args.afi, args.k_n)
