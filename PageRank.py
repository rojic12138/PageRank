#2021年10月29日20:54:13
#罗皓 互联网数据挖掘第一次作业
import time
time_start=time.time()
print("Start to create list")
PR={} #str to float
#Graph=[[0 for i in range(305)] for j in range(6000)] #Graph[i][j] 表示i到j有连接 Test
Graph=[[0 for i in range(105)] for j in range(500010)] #Graph[i][j] 表示i到j有连接
Titles=['rojic' for i in range(500010)] #str
titles_to_index={}#str to int
out_num={} #str to int 

#mean_out_num=0 #平均出度 抽样显示一个页面平均指向97个页面

file_path_in='wikiZN.txt'
file_in=open(file_path_in,'r',encoding='utf-8')
file_path_out='Output.txt'
file_out=open(file_path_out,'w',encoding='utf-8')
           
#max_out=0 #最大出度 抽样显示一个页面最多指向1800个页面
count=0 #已有标题数
time_create_list=time.time()
full=False
def init(s):#初始化一个标题
    global count
    global full
    if(s not in Titles):
        PR[s]=1
        Titles[count]=s
        titles_to_index[s]=count
        count+=1
        out_num[s]=0
        if(count%5000==0):
            print(count,'words')
            #print(max_out) 
        if(count>=500000):
            full=True    
           
from_str="" #页面的标题
to_str="" #link到的页面的标题
flag=False#下一行是页面的标题

#建立图
print("Start to create graph")
for line in file_in.readlines():
    if(full):
        break
    if(flag):
        flag=False
        from_str=line[:-2] #最后一个字符是冒号:，去掉 
        init(from_str)
        #print(from_str)
        continue
    if(line=='\n'):#只有换行，下一行一定是新页面的标题
        flag=True
        continue
    else: #查找link到的页面
        from_index=line.find("<a href=\"")
        while(from_index!=-1):
            if(out_num[from_str]>=100):
                break
            to_index=line.find("\">",from_index)
            to_str=line[from_index+9:to_index]
            init(to_str)
            from_index=line.find("<a href=\"",to_index)
            Graph[titles_to_index[from_str]][out_num[from_str]]=titles_to_index[to_str]
            out_num[from_str]+=1
            #max_out=max(max_out,out_num[from_str])
    #mean_out_num+=out_num[from_str]
time_create_graph=time.time()            
#print(mean_out_num/count)

#初始化
for k,v in PR.items():
    PR[k]=1/count
    
#遍历字典，修改PR  
epoch=50
d=0.85 #阻尼系数
diff=0 #最大改变情况，用来控制拟合程度
print("Start to calculate PageRank")
for e in range(epoch):    
    diff=0          
    tmp_PR={} 
    for k,v in PR.items():
        tmp_PR[k]=1-d
    for i in range(count):
        for j in range(out_num[Titles[i]]):
            tmp_PR[Titles[Graph[i][j]]]+=d*PR[Titles[i]]/out_num[Titles[i]]
    for k,v in PR.items():
        diff=max(diff,abs(tmp_PR[k]-PR[k])/PR[k])
        
    print(diff)
    PR=tmp_PR
    print(e+1,'th epoch')
    if(diff<0.001):
        break
time_PageRank=time.time()    

#输出
print("Time of creating list: "+str(time_create_list-time_start))
print("Time of creating graph: "+str(time_create_graph-time_create_list))
print("Time of calculating PageRank: "+str(time_PageRank-time_create_graph))
a=sorted(PR.items(),key=lambda x:x[1],reverse=True)
for i in range(len(a)):
    file_out.write(a[i][0]+"\t"+str(a[i][1])+'\n')

file_in.close()
file_out.close()