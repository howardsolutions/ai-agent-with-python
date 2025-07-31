from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file

print("=== get_file_content tests ===")
print("1. get_file_content('calculator', 'main.py')")
print(get_file_content("calculator", "main.py"), end="\n\n")

print("2. get_file_content('calculator', 'pkg/calculator.py')")
print(get_file_content("calculator", "pkg/calculator.py"), end="\n\n")

print("3. get_file_content('calculator', '/bin/cat')")
print(get_file_content("calculator", "/bin/cat"), end="\n\n")

print("4. get_file_content('calculator', 'pkg/does_not_exist.py')")
print(get_file_content("calculator", "pkg/does_not_exist.py"), end="\n\n")

print("=== get_files_info tests ===")
print("1. get_files_info('calculator', '.')")
print(get_files_info("calculator", "."), end="\n\n")

print("2. get_files_info('calculator', 'pkg')")
print(get_files_info("calculator", "pkg"), end="\n\n")

print("3. get_files_info('calculator', '/bin')")
print(get_files_info("calculator", "/bin"), end="\n\n")

print("4. get_files_info('calculator', '../')")
print(get_files_info("calculator", "../"), end="\n\n")

print("=== write_file tests ===")
print("1. write_file('calculator', 'lorem.txt', 'wait, this isn't lorem ipsum')")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), end="\n\n")

print("2. write_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet')")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), end="\n\n")

print("3. write_file('calculator', '/tmp/temp.txt', 'this should not be allowed')")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), end="\n\n")
