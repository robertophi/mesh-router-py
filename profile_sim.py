import os

print("Running code...")
os.system('python -m cProfile -o profile_description.cprof main.py')
print("Profiling done...")
os.system('pyprof2calltree -k -i profile_description.cprof')
