from certificates import *
from plot import *
from glob import *

print("Program is running.")
domain_files = glob('websites/*.txt')

for filename in domain_files:
    create_certificate_file(filename)

date_files = glob('dates/*.txt')
produce_date_graphs(date_files)
produce_length_graph(date_files)

print("Program is done.")   




