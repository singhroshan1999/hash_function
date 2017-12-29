'''
made by ROSHAN SINGH
pseudo indexed character based number string fingerprinting HASH
HASHID-1

'''
import time
def getFileSize(f):
    pos=fp.tell()
    f.seek(0,2)
    size = f.tell()
    f.seek(pos)
    return size

def cluster(strin,pos):#upto 256bytes
    if pos!=0:
         xor=((((((pos)*(1103515245)**2+123456)%((0xffffffff)**2+1))//(ord(strin[0])+2))*(1103515245)**2+123456)%((0xffffffff)**2+1))
    else:
         xor=((ord(strin[0])*(1103515245)**2+12345)%((0xffffffff)**2+1))#
    for i in range(1,len(strin)):
        xor=xor^((((((i+pos)*(1103515245)**2+123456)%((0xffffffff)**2+1))//(ord(strin[i])+2))*(1103515245)**2+123456)%((0xffffffff)**2+1))    # have not tested wheather i should raise 123456's power 
    return xor                                                                                                                                                                                                                  # this might make my algo vulnerable to collision. this is in TODO list
# obsolate node
def node(numl,pos):#upto 8 clusters
    xor=((numl[0]*(1103515245)**2+12345)%((0xffffffff)**2+1))#
    for i in range(1,len(numl)):
        xor=xor^((((((i+pos)*(1103515245)**2+123456)%((0xffffffff)**2+1))//(numl[i]+2))*(1103515245)**2+123456)%((0xffffffff)**2+1))
    return xor
######
def block(numl,pos):#upto upto 8 nodes
    if pos!=0:
         xor=((((((pos)*(1103515245)**3+123456)%((0xffffffff)**3+1))//(numl[0]+2))*(1103515245)**3+123456)%((0xffffffff)**3+1))
    else:
         xor=((numl[0]*(1103515245)**3+12345)%((0xffffffff)**3+1))#
    for i in range(1,len(numl)):
        xor=xor^((((((i+pos)*(1103515245)**3+123456)%((0xffffffff)**3+1))//(numl[i]+2))*(1103515245)**3+123456)%((0xffffffff)**3+1))
    return xor
def prim_chksum(numl,pos):#
    if pos!=0:
        xor=((((((pos)*(1103515245)**4+123456)%((0xffffffff)**4+1))//(numl[0]+2))*(1103515245)**4+123456)%((0xffffffff)**4+1))
    else:
        xor=((numl[0]*(1103515245)**4+12345)%((0xffffffff)**4+1))#
    for i in range(1,len(numl)):
        xor=xor^((((((i+pos)*(1103515245)**4+123456)%((0xffffffff)**4+1))//(numl[i]+2))*(1103515245)**4+123456)%((0xffffffff)**4+1))
    return xor
def file_hash(fp):#upto any block
    siz=getFileSize(fp)
    clustered=[]
#    noded=[]
    blocked=[]
    prim_chksumed=0
    t11=0
    t22=0
    t33=0

    for  i in range(siz/256+1):
        
        if len(blocked)==8:
            t1=time.time()
            prim_chksumed^=prim_chksum(blocked,i*16384)#i*<strin_len>*<numlin_len>**2
            blocked=[]
            t1-=time.time()
            t11+=t1
        if len(clustered)==8:
            t2=time.time()
            n=block(clustered,(i*2048))#i*<strin_len>*<numlin_len>
            blocked.append(n)
            clustered=[]
            t2-=time.time()
            t22+=t2

        a=fp.read(256)
        if a=='':
            break

        t3=time.time()
        clustered.append(cluster(a,i*256)) # this make slow
        t3-=time.time()
        t33+=t3
    print 'total cluster() time:',-t33,'\ntotal block() time:',-t22,'\ntotal prime_chksum() time:',-t11
    if len(clustered)!=0 :
#        noded.append(node(clustered,(i*)))
        blocked.append(block(clustered,(i*2048)))
        prim_chksumed^=prim_chksum(blocked,(i*16384))
    print prim_chksumed#####
    return prim_chksumed
while True:

    fp=open(raw_input('Enter file name:'),'rb')
    t=time.time()
    print '\n',hex(file_hash(fp))[2:].upper(),'\n'
    fp.close()
    t-=time.time()
    print 'total time escaped:',-t
    if raw_input('Enter "1" to enter more:') == '1':
        pass
    else:
        break
print '''
      ___           ___           ___           ___                       ___     
     /\__\         /\  \         /\  \         /\__\          ___        /\  \    
    /:/  /        /::\  \       /::\  \       /:/  /         /\  \      /::\  \   
   /:/__/        /:/\:\  \     /:/\ \  \     /:/__/          \:\  \    /:/\:\  \  
  /::\  \ ___   /::\~\:\  \   _\:\~\ \  \   /::\  \ ___      /::\__\  /:/  \:\__\ 
 /:/\:\  /\__\ /:/\:\ \:\__\ /\ \:\ \ \__\ /:/\:\  /\__\  __/:/\/__/ /:/__/ \:|__|
 \/__\:\/:/  / \/__\:\/:/  / \:\ \:\ \/__/ \/__\:\/:/  / /\/:/  /    \:\  \ /:/  /
      \::/  /       \::/  /   \:\ \:\__\        \::/  /  \::/__/      \:\  /:/  / 
      /:/  /        /:/  /     \:\/:/  /        /:/  /    \:\__\       \:\/:/  /  
     /:/  /        /:/  /       \::/  /        /:/  /      \/__/        \::/__/   
     \/__/         \/__/         \/__/         \/__/                     ~~       
     '''
raw_input()
