from opencc import OpenCC

cc=OpenCC('t2s')

file_path_in='wiki.txt'
file_in=open(file_path_in,'r',encoding='utf-8')
file_path_out='wikiZN.txt'
file_out=open(file_path_out,'w',encoding='utf-8')
count=0
for line in file_in.readlines():
    file_out.write(cc.convert(line))
    count+=1
    if(count%5000==0):
        print(count,"lines")
    if(count>3500000 and line=='\n'):
        break
    
file_in.close()
file_out.close()