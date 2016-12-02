#!/usr/bin/python

import os
from os.path import join
from subprocess import check_output

class MessageGenerator:

	def generate_for_package(self, package_name):
		print 'Generating messages for package {}'.format(package_name)

	def generate_for_metamessage(self, package_name, message_name):
		print 'Gera a mensagem somente de %s' % message_name
		package_path = check_output(["rospack", "find", package_name])[:-1]
		splitted_message_name = message_name.split('/')
		if len(splitted_message_name) == 1:
			message_name = splitted_message_name[0]
		else:
			message_name = splitted_message_name[len(splitted_message_name) - 1]
		found_file = self.__locate(message_name + '.mmsg', package_path)
		if found_file:
			f = open(found_file, 'r')
			file_content = f.read()
			lines = file_content.split('\n')
			msg_file = open(package_path + "/msg/" + message_name + ".msg", "w")
			msg_file.write("# ====== DO NOT MODIFY! AUTOGENERATED FROM A META MESSAGE DEFINITION ======\n\n")
			if len(lines) > 0 and "extends" in lines[0]:
				first_line = lines[0].replace("extends", "").replace(" ", "")
				extends_from = first_line.split(',')
				file_content = ""
				for message in extends_from:
					message_content = check_output(["rosmsg", "show", message])
					if "Unable to load msg" in message_content:
						print message_content
						sys.exit()
					message_lines = message_content.split('\n')
					for line in message_lines:
						if not line.startswith(' '):
							msg_file.write(line + "\n")
				for i in range(1, len(lines)):
					msg_file.write(lines[i] + "\n")
			msg_file.write(file_content)
			msg_file.close()
			f.close()
		else:
			print 'File not found'

	def __locate(self, file_name, root = os.curdir):
		for c in os.listdir(root):
			if c.startswith("."):
				continue
			candidate = os.path.join(root, c)
			if not os.path.isfile(candidate):
				candidate = self.__locate(file_name, candidate)
				if candidate is not None:
					return candidate
			elif c == file_name:
				   return candidate
		return None