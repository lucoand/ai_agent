from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file

# test1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(test1)
#
# test2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(test2)
#
# test3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(test3)

# test4 = get_files_info("calculator", ".")
# print(test4)
#
# test5 = get_files_info("calculator", "pkg")
# print(test5)
#
# test6 = get_files_info("calculator", "/bin")
# print(test6)
#
# test7 = get_files_info("calculator", "../")
# print(test7)

# test8 = get_file_content("calculator", "main.py")
# print(test8)
#
# test9 = get_file_content("calculator", "pkg/calculator.py")
# print(test9)
#
# test10 = get_file_content("calculator", "/bin/cat")
# print(test10)

test11 = run_python_file("calculator", "main.py")
print(test11)

test12 = run_python_file("calculator", "tests.py")
print(test12)

test13 = run_python_file("calculator", "../main.py")
print(test13)

test14 = run_python_file("calculator", "nonexistent.py")
print(test14)
