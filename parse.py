import matplotlib.pyplot as plt
import numpy as np
import os
import re

def collect(path):
    txtFiles = os.listdir("data/" + path)
    latency = {"startup" : 0, "display" : 0, "displayObjects": 0, "objects" : 0, "downloadS3" : 0, "size" : 0}
    for file in txtFiles:
        with open("data/" + path + file, 'r') as f:
            temp = []
            for line in f:
                if (re.search(r"latency|objects in current scene|bytes size", line)):
                    temp.append(line)
            latency['startup'] += int(re.search(r': [0-9]+', temp[0]).group(0).split(' ')[1])
            print(temp[0]) #start up
            latency['display'] += int(re.search(r': [0-9]+', temp[-1]).group(0).split(' ')[1]) - int(re.search(r': [0-9]+', temp[-2]).group(0).split(' ')[1])
            print(temp[-1]) #display data
            print(temp[-2]) #display each object in scene
            latency['displayObjects'] += int(re.search(r': [0-9]+', temp[-2]).group(0).split(' ')[1])

            print(temp[-3]) #objects in current scene
            latency['objects'] += int(re.search(r': [0-9]+', temp[-3]).group(0).split(' ')[1])
            print(temp[-4]) #download file s3
            latency['downloadS3'] += int(re.search(r': [0-9]+', temp[-4]).group(0).split(' ')[1])

            latency['size'] += int(re.search(r'= [0-9]+', temp[1]).group(0).split(' ')[1])
            print(temp[1]) #size
    latency['downloadS3'] = round(latency['downloadS3']/3, 2)
    latency['display'] = round(latency['display']/3, 2)
    latency['startup'] = round(latency['startup']/3, 2)
    latency['objects'] = round(latency['objects']/3, 2)
    latency['displayObjects'] = round(latency['displayObjects']/3, 2)
    latency['size'] = round(latency['size']/3/1024/1000, 3) #gives MB
    return latency

def plot (dataList : list):
    #https://matplotlib.org/3.5.0/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    labels = ['Small', 'Medium', 'Large']
    # small = dataList[0]
    # medium = dataList[1]
    # large = dataList[2]
    small = dataList[0]
    medium = dataList[1]
    large = dataList[2]
    startup = []
    display = []
    displayObjects = []
    objects = []
    downloadS3 = []
    size = []
    for data in [small, medium, large]:
        startup.append(data['startup'])
        display.append(data['display'])
        displayObjects.append(data['displayObjects'])
        objects.append(data['objects'])
        downloadS3.append(data['downloadS3'])
        size.append(data['size'])
    x = np.arange(len(labels)) #bar locations
    width = 0.1 #width of the bars

    fig, ax = plt.subplots()
    startupLatency = ax.bar(x - width/2, startup, width, label='Start Up')
    displayLatency = ax.bar(x + width/2, display, width, label="Display Set Up")
    downloadS3Latency = ax.bar(x - (width * 1.5), downloadS3, width, label='Download S3')
    displayObjects = ax.bar(x + (width * 1.5), displayObjects, width, label='Displaying Objects')
    # sizeMb = ax.bar(x + (width * 2.5), size, width, label="Size in MB")
    

    ax.set_ylabel('Latency')
    ax.set_title('Mean Latency for Different Sizes')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(startupLatency, padding=3)
    ax.bar_label(displayLatency, padding=3)
    ax.bar_label(downloadS3Latency, padding=3)
    ax.bar_label(displayObjects, padding=3)
    # ax.bar_label(objectsNum, padding=3 )
    # ax.bar_label(sizeMb, padding = 3)

    fig.tight_layout()

    plt.show()

    fig2, ax2 = plt.subplots()
    ax2.set_axis_off()
    
    rowHeaders = ('Small', 'Medium', 'Large')
    colHeaders = ("Number of Objects", "Size of File (MB)")  
    ax2.set_title('Mean Data for Different Sizes', fontweight="bold")

    values = []
    for r in range(3):
        temp = []
        temp.append(objects[r])
        temp.append(size[r])
        values.append(temp)
           
    table = ax2.table(cellText = values,
                    rowLabels = rowHeaders,
                    colLabels= colHeaders,
                    cellLoc='center',
                    loc='upper left')
    plt.show()

dataList = []
types = ['Small/', 'Medium/', 'Large/']

for i in types:
    dataList.append(collect(i))
plot(dataList)



