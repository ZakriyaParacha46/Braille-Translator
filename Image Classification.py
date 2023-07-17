import numpy as np
import cv2  
from matplotlib import pyplot as plt
import math

#helping functions
def roundto(num):
    return float("{:0.3f}".format(num))

def getLesion(mask,image):
    maxind,minind,count=[0,0],[1000,1000],0

    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if(mask[i][j]):
                count+=1
                if (i<minind[0]):minind[0]=i
                if (j<minind[1]):minind[1]=j
                if (i>maxind[0]):maxind[0]=i
                if (j>maxind[1]):maxind[1]=j

    return count,image[minind[0]:maxind[0],minind[1]:maxind[1]]

def distance(p1,p2):
    sum=0
    for i in p1.keys():
        sum+=(p1[i]-p2[i])**2 
    return roundto(math.sqrt(sum))

#parameter extraction
def Symmetry(img):
    size=img.shape[0]*img.shape[1]
    count,croped=getLesion(img,img)
    c_x,c_y=croped.shape

    h1,h2 = croped[0:math.ceil(c_x/2),:],croped[math.floor(c_x/2):,:]
    v1,v2 = croped[:,0:math.ceil(c_y/2)],croped[:,math.floor(c_y/2):]

    h2_fliped= h2*0
    v2_fliped= v2*0

    for i in range(h2.shape[0]):
        for j in range(h2.shape[1]):
            h2_fliped[i][j]=h2[-i][j]

    for i in range(v2.shape[0]):
        for j in range(v2.shape[1]):
            v2_fliped[i][j]=v2[i][-j]

    #cv2.imshow("Horizontal",h1^h2_fliped)
    #cv2.imshow("Vertical  ",v1^v2_fliped)
    #cv2.waitKey()

    xoredH= np.count_nonzero(h1^h2_fliped)
    xoredV= np.count_nonzero(v1^v2_fliped)
    return roundto((count/size)*100),roundto((xoredH/size)*100),roundto((xoredV/size)*100)

def getcolors(img, mask):
    s,lesion=getLesion(mask,img)
    ## PDF ##
    histogram = np.zeros((3,256),dtype=np.uint32)
    for i in range(lesion.shape[0]):
        for j in range(lesion.shape[1]):
            for c in range(histogram.shape[0]):
                ind=lesion[i][j][c]
                if(ind!=255):
                    histogram[c][ind]+=1

    #plt.title("PDF RGB")
    #plt.bar([i for i in range(256)],histogram[0],color=['red'])   
    #plt.bar([i for i in range(256)],histogram[1],color=['green'])        
    #plt.bar([i for i in range(256)],histogram[2],color=['blue'])   
    #plt.show()

    return roundto(np.std(histogram[0])),roundto(np.std(histogram[1])),roundto(np.std(histogram[2]))

def getfiledata(fileadd):
    Legends = {'0':'S','1': 'A', '2':'M'}
    filedata= {"S":[], "A":[],"M":[]}
    with open(fileadd, "r") as f:
        lines= f.readlines()
        lines.pop(0)
        for line in lines:
            if(line.split('||')[0]=='\n'):break 
            filedata[Legends[line.split('||')[3].strip()]].append(line.split('||')[1].strip())
        return filedata

#CODE
files= getfiledata(fileadd)
parameter= {'count':0,"Hs":0,"Vs":0,'R':0,'G':0,'B':0}

lst=[]
for Te in files.keys():
    avg = {'count':0,"Hs":0,"Vs":0,'R':0,'G':0,'B':0}
    c   = 0 
    for imgno in files[Te]:
        c=c+1
        fileimg="Dataset/{imgno}/{imgno}_Dermoscopic_Image/{imgno}.bmp".format(imgno=imgno)
        filemask="Dataset/{imgno}/{imgno}_lesion/{imgno}_lesion.bmp".format(imgno=imgno)
        image = cv2.imread(fileimg, 1)
        mask  = cv2.imread(filemask,-1)
        parameter['count'],parameter['Hs'],parameter['Vs']=Symmetry(mask)
        parameter['R'],parameter['G'],parameter['B']=getcolors(image,mask)
        #average
        for i in avg.keys():avg[i]+=parameter[i]
        print(Te ,parameter)

    for i in avg.keys():avg[i]=roundto(avg[i]/c)
    lst.append(avg)
    print(Te, avg)


#lst=[{'count': 11.233, 'Hs': 0.773, 'Vs': 0.809, 'R': 389.544, 'G': 404.1, 'B': 432.367},
#{'count': 22.722, 'Hs': 3.582, 'Vs': 3.467, 'R': 760.159, 'G': 833.47, 'B': 927.186},
#{'count': 64.94, 'Hs': 7.932, 'Vs': 9.616, 'R': 2166.262, 'G': 1866.898, 'B': 1311.494}]
#testing
print('S-A',distance(lst[0],lst[1]))
print('S-M',distance(lst[0],lst[2]))
print('A-M',distance(lst[1],lst[2]))