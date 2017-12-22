import os
import csv
import shutil
import time
from hashlib import md5

print 'processing...'

# init parameter
resourceDir = os.environ['HOME'] + '/Desktop/resources/'
outputDir = resourceDir + '__outputs__/'
supports = {'music': ['mp3'], 'story': ['mp3'], 'sound': ['mp3'], 'face': ['mp4']}
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
model = 'ZN322311'
resourceTable = [('model', 'domain', 'name', 'url', 'checksum', 'size', 'created_at', 'updated_at')]

# check directories
if not os.path.exists(resourceDir):
    print 'FATAL: Resource Directory non existed!'
    exit()
os.path.exists(outputDir) and shutil.rmtree(outputDir)
os.mkdir(outputDir)

# traverse files to rename it and prepare data
for domain in os.listdir(resourceDir):
    # DOMAIN
    if domain in supports.keys():
        os.mkdir(outputDir + domain)

        items = os.listdir(resourceDir + domain)
        items.sort()
        for item in items:
            # NAME
            name, suffix = item.split('.')

            if suffix in supports[domain]:
                with open(resourceDir + domain + '/' + item, 'rb') as inputFile:
                    # CHECKSUM
                    md5Calculator = md5()
                    md5Calculator.update(inputFile.read())
                    checksum = md5Calculator.hexdigest()

                    # SIZE
                    inputFile.seek(os.SEEK_SET, os.SEEK_END)
                    size = inputFile.tell() / 1000

                    # URL
                    url = 'jett/resources/%s/%s.%s' % (domain, checksum, suffix)

                    # copy file and rename it
                    with open(outputDir + domain + '/%s.%s' % (checksum, suffix), 'wb') as outputFile:
                        inputFile.seek(os.SEEK_SET)
                        outputFile.write(inputFile.read())

                    resourceTable.append((model, domain.title(), name, url, checksum, str(size), now, now))

# output csv for import to mysql
with open(outputDir + 'resources.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(resourceTable)
    csvFile.close()

print 'Done!'
