from ..libs import *



def converto_time_json_json(position,trellis_len,len_signal,sr,target_sr):
    return int((position/trellis_len)*(len_signal/sr)*(target_sr))


def convert_json_json(file_name,word_segments,trellis_len,len_signal,sr,convert_function,target_sr,output_folder,name):
    f=open(file_name,"rb")
    data=json.load(f)
    
    word_sentence=[]
    word=[]
    result=[]
    index=0
    count=0
    
    for arr in data:
        num_wor=0
        for w in arr['l']:
            target=w['d']
            lis=w['d'].split(' ')
            for item in lis:
                word.append(item)
                num_wor +=1
        word_sentence.append(num_wor)
        
    for i in range(len(word_sentence)):
        result.append({})
        result[index]['s']=0
        result[index]['e']=0
        result[i]['l']=[]

    i=0
    for w in word:
        result[index]['l'].append({})
        result[index]['l'][count]['s']=convert_function(word_segments[i].start,trellis_len,len_signal,sr,target_sr)
        result[index]['l'][count]['d']=w
        result[index]['l'][count]['e']=convert_function(word_segments[i].end,trellis_len,len_signal,sr,target_sr)
        count += 1
        if("’" in w):
            i += 2 
        else :
            i +=1 
        if(count==word_sentence[index]):
            result[index]['s']=result[index]['l'][0]['s']
            result[index]['e']=result[index]['l'][-1]['e']
            index +=1 
            count = 0
    
    with open(os.path.join(output_folder,name), "w",encoding='utf-8') as outfile:
        json.dump(result, outfile,ensure_ascii=False)