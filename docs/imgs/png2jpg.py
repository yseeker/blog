import glob
import subprocess

f = glob.glob("*.png")

for name in f:
    #print(name, f"{name.split('.')[0]}.jpg")
    subprocess.run(f"mv {name} {name.split('.')[0]}.jpg", shell = True)
