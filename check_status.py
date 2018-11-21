#!/usr/bin/python
import argparse
import time
import json
import subprocess
import os
import os.path

def create_image(binpath, bucketname):
	filename = os.path.basename(binpath)
	name, ext = os.path.splitext(filename)


	arg_image=list()
	arg_image.append(os.path.join(os.environ['AWS_FPGA_REPO_DIR'],'SDAccel','tools',
				'create_sdaccel_afi.sh'))
	arg_image.append('-xclbin=%s'%binpath)
	arg_image.append('-o=%s'%name)
	arg_image.append('-s3_bucket=%s'%bucketname)
	arg_image.append('-s3_dcp_key=dcp_folder')
	arg_image.append('-s3_logs_key=logs')
	
	p_image= subprocess.call(arg_image)
	return p_image
def check_status(afi_file):
	with open(afi_file,'r') as f:
		d_afi = json.load(f)

	afi_id = d_afi['FpgaImageId']

	arg_status = list()
	arg_status.append('aws')
	arg_status.append('ec2')
	arg_status.append('describe-fpga-images')
	arg_status.append('--fpga-image-ids')
	arg_status.append(afi_id)
	while True:
		p_status = subprocess.Popen(arg_status, stdout=subprocess.PIPE)
		p_status.wait()
		out, err = p_status.communicate()
		j_st = json.loads(out)
		code = j_st["FpgaImages"][0]["State"]["Code"]
		if code =='pending':
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(10)

		#	print("Image is pending.")
		#	time.sleep(60)
		elif code =='available':
			print("Image available online")
			print("Finished")
			break
		else:
			print("Unknow code, please fix it.")
			break

def main(binpath, bucketname):


	# STEP ONE
	# CREATE IMAGE
	
	to_aws=os.path.join(os.getcwd(), "to_aws")
	if os.path.exists(to_aws):
		print("directory 'to_aws' is existed")
		fileInterest = [f for f in os.listdir('.') if f.endswith('afi_id.txt')]
		if not len(fileInterest) == 1:
			print("There is no *afi_id.txt file or more than one, please delete them and retry.")
			return
		else:
			print("There is file %s in current dir, checking its status..."%fileInterest[0])
			check_status(fileInterest[0])
	else:
		status = create_image(binpath, bucketname)
		if status ==0:
			print("create image successfully.")
			fileInterest = [f for f in os.listdir('.') if f.endswith('afi_id.txt')]
			if not len(fileInterest) == 1:
				print("There is no *afi_id.txt file or more than one, please check it.")
				return
			else:
				check_status(fileInterest[0])
		else:
			print("create image failed.")
			return


if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Check the status of the image on AWS, environment variable 'AWS_FPGA_REPO_DIR', 'AWS_PLATFORM' and 'USER' should be defined.")
	parser.add_argument('--bin', help="Kernel binary file, *.xclbin")
	args = parser.parse_args()
	if args.bin==None:
		parser.print_help()
	elif os.environ['AWS_FPGA_REPO_DIR'] == None:
		print("env variable 'AWS_FPGA_REPO_DIR' is not defined.")
	elif os.environ['AWS_PLATFORM'] == None:
		print("env variable 'AWS_PLATFORM' is not defined.")
	elif os.environ['USER'] == None:
		print("env variable 'USER' is not defined.")
	else:
		main(args.bin, os.environ['USER'])
