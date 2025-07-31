from functions.write_file import write_file

print("1. write_file('calculator', 'lorem.txt', 'wait, this isn't lorem ipsum')")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), end="\n\n")

print("2. write_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet')")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), end="\n\n")

print("3. write_file('calculator', '/tmp/temp.txt', 'this should not be allowed')")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), end="\n\n")
