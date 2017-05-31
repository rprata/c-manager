import subprocess as sub
import threading

program = "#include <stdio.h>\n"
program += "int main()\n"
program += "{\n"
program += 	"\tchar i;\n"
program += 	"\tint n = 20;\n"
program += 	"\tfor(%s)\n"
program += 		"\t\tprintf(\"-\");\n"
program += 	"\tprintf(\"\\n\");\n"
program += 	"\treturn 0;\n"
program += "}"

new_program_file = "new.c"
line = " i = 0; i < n; i-- "
possible_chars = ['+', '-', '=', '<', '>', ' ', 'n', 'i']

proc_list = []
valid_list = []
black_list = []

def create_new_output (line, p, i):
	s = ""
	for k in range(0, len(line)):
		if (k == i):
			s += p
		else:
			s += line[k];
	return s;


def save_in_file(new_program):
	file = open(new_program_file, "w")
	file.write(new_program)
	file.close()

def try_to_compile():
	p = sub.Popen(['gcc', new_program_file],stdout=sub.PIPE,stderr=sub.PIPE)
	output, errors = p.communicate()
	return output, errors

def check_if_is_running(p, expression):
	if (p.poll() != -1):
		if (p in proc_list):
			pass
		else:
			black_list.append(expression)
			p.kill()

def run_program_to_check(expression):
	try:
		p = sub.Popen(['./a.out > /dev/null '], shell=True)
		t = threading.Timer(1.0, check_if_is_running, [p, expression])
		t.start()
		output, errors = p.communicate()
		proc_list.append(p)
		return output, errors
	except:
		return "";

def run_program():
	try:
		p = sub.Popen(['./a.out'],stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
		output, errors = p.communicate()
		return output
	except:
		return "";

def create_possible_programs():
	for p in possible_chars:
		i = 0;
		while i < len(line):
			out = create_new_output(line, p, i)
			save_in_file(program % out)
			res = try_to_compile()
			if (len(res[1]) == 0):
				# first check if a infinity loop will happens
				valid_list.append(out)
				run_program_to_check(out)
			i += 1

def find_solution():
	# finding solution
	for out in valid_list:
		if (out in black_list):
			pass
		else:
			save_in_file(program % out)
			res = try_to_compile()
			if (len(res[1]) == 0):
				f = run_program()
				if (len(f) == 21):
					print "============================"
					print program % out
	print "============================"
	
create_possible_programs()
sub.call(["killall", "a.out"])
find_solution()