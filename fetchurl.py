#! /usr/bin/env python
import sys
import os
import zipfile
import tarfile
import hashlib
import shutil
import urlgrabber.grabber
from urlgrabber.progress import text_progress_meter

def printusage(argv0):
  print "Usage: " + argv0 + " URL [OPTIONS]"
  print "\t-c sha256, --checksum sha256\tCompare downloaded file with a SHA-256 checksum."
  print "\t-x, --extract\t\t\tExtract the downloaded file if possible."
  print "\t-o, --overwrite\t\t\tOverwrite a potentially existing directory (only if -x is provided)."
  print "\t-a, --append\t\t\tAppend with a potentially existing directory (only if -x is provided)."
  print "\t-d, --discard\t\t\tDiscard extracting if the target directory already exists (only  if -x is provided)."
  print "\t-h, --help\t\t\tPrint help."
  print "\t-v, --verbose\t\t\tEnable verbosity."
  return

def fsha256(fname, blockSize=2**20):
  f = open(fname)
  s = hashlib.sha256()
  while True:
    data = f.read(blockSize)
    if not data:
      break
    s.update(data)
  return s.hexdigest()

def vprint(txt, verbose = True):
  if verbose:
    print(txt)
  return

if len(sys.argv) < 2:
  printusage(sys.argv[0])
  sys.exit(1)

checksum = None
verbose = False
extract = False
diraction = None
for i in range(2, len(sys.argv)):
  if sys.argv[i] == "-c" or sys.argv[i] == "--checksum":
    i+=1
    checksum = sys.argv[i]
  elif sys.argv[i] == "-x" or sys.argv[i] == "--extract":
    extract = True
  elif sys.argv[i] == "-o" or sys.argv[i] == "--overwrite":
    diraction = "o"
  elif sys.argv[i] == "-a" or sys.argv[i] == "--append":
    diraction = "a"
  elif sys.argv[i] == "-d" or sys.argv[i] == "--discard":
    diraction = "d"
  elif sys.argv[i] == "-v" or sys.argv[i] == "--verbose":
    verbose = True
  elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
    printusage(sys.argv[0])
    sys.exit(0)
  else:
    print "ERROR: Unknown option " + sys.argv[i] + "."
    printusage(sys.argv[0])
    sys.exit(1)

fname = urlgrabber.urlgrab(sys.argv[1], filename=None, reget=None, progress_obj=urlgrabber.progress.text_progress_meter(), ssl_ca_cert="/etc/ssl/certs/ca-certificates.crt")

if checksum:
  fchecksum = fsha256(fname)
  vprint("SHA256: " + fchecksum, verbose)
  if checksum != fchecksum:
    print("ERROR: invalid checksum '" + fchecksum + "', '" + checksum + "' was expected.")
    sys.exit(1)

if not extract:
  vprint("Downloaded to " + fname, verbose)
  sys.exit(0)

extractor = None
dirname = None
if zipfile.is_zipfile(fname):
  extractor = zipfile.ZipFile(fname)
  dirname = fname
  if os.path.splitext(dirname)[1] == ".zip":
    dirname = os.path.splitext(dirname)[0]
elif tarfile.is_tarfile(fname):
  extractor = tarfile.open(fname)
  dirname = fname
  cleaned = False
  while not cleaned:
    splitted = os.path.splitext(dirname)
    if len(splitted) < 2:
      cleaned = True
    elif splitted[1] == ".gz" or splitted[1] == ".bz2":
      dirname = splitted[0]
    elif splitted[1] == ".tar" or splitted[1] == ".tgz":
      dirname = splitted[0]
      cleaned = True
    else:
      cleaned = True

if not dirname or not extractor:
  vprint("ERROR: Cannot extract archive " + fname, verbose)
  sys.exit(1)

if os.path.exists(dirname):
  if not diraction:
    diraction = raw_input("WARNING: The directory " + dirname + " already exists. Overwrite [o], Append [a] or Discard [d] ? ").lower()
if diraction == "o":
  vprint("Removing the directory " + dirname, verbose)
  shutil.rmtree(dirname)
elif diraction == "d":
  vprint("The directory " + dirname + " will stay untouched and the archive " + fname + " will not be deleted.\nLeaving with the exit code 0.", verbose)
  sys.exit(0)
elif diraction != "a":
  print("ERROR: Unknown action " + diraction)
  sys.exit(1)
vprint("Extracting to " + dirname, verbose)
extractor.extractall(dirname)
os.remove(fname)
l = os.listdir(dirname)
if len(l) == 1 and os.path.isdir(dirname + "/" + l[0]):
  subdir = dirname + "/" + l[0]
  vprint("Moving " + subdir + " to " + dirname, verbose)
  for f in os.listdir(subdir):
    os.rename(subdir + "/" + f, dirname + "/" + f)
  shutil.rmtree(subdir)
vprint("Dowloaded and extracted to " + dirname, verbose)
sys.exit(0)

