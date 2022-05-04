import os
import csv
import glob
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from operator import itemgetter
class KEY_MANAGER():
    
    def __init__(self):
        self.raw_word = ''
        
    
    def add_col_to_csv(self,csvfile,fileout,new_list):
        with open(csvfile, 'r',encoding="utf8") as read_f, \
            open(fileout, 'w', newline='',encoding="utf8") as write_f:
            csv_reader = csv.reader(read_f)
            csv_writer = csv.writer(write_f)
            i = 0
            for row in csv_reader:
                row.append(new_list[i])
                csv_writer.writerow(row)
                i += 1      
                
    def loadfile(self,keyword):
        list_all_files = [] 
        word = keyword.lower()
                        
        for i in range(19):
            list_web = ["assist-football","birminghammail","eftfootball","eurosport","football-kapook","football365","footballaddrict","footballhits98","footballmoment","goal","shotongoal","siamsport","skysports","sport-mthai","sportbible","sportsmole","standard","talksport","thairath"]
            all_files = glob.glob(f"DataCSV/{list_web[i]}/*.csv")
            for k in range(len(all_files)):
                list_all_files.append(all_files[k])
        list_df = pd.concat((pd.read_csv(f,encoding = 'utf-8',index_col=0).assign(Keyword = keyword) for f in list_all_files),ignore_index = True)   
        if "sentiment" in list_df:
            list_df.pop("sentiment")
        list_num_drop = []
        list_word_count = ["Count-keyword"]
        num = 0
        for j in list_df.Contents:
            if word not in j.lower():
                list_num_drop.append(num)
            else:
                contents = j.lower()
                word_count = contents.count(word)
                list_word_count.append(word_count)
                self.raw_word += j+" "
            num += 1
        list_keyword = list_df.drop(list_num_drop)    
        
        if not os.path.exists(f'./DataKeyword'):                    
            os.mkdir(f'./DataKeyword')  
            print("CreteFolder Successed")
          
        list_keyword.to_csv(f"./DataKeyword/_{word}.csv",index=False)   
        
        self.add_col_to_csv(f"./DataKeyword/_{word}.csv",f"./DataKeyword/{word}.csv",list_word_count)
        
        self.relate_web(keyword)
        
    def relate_web(self,keyword):
        ## nlp
        Keyword = keyword.lower()
        raw_word = self.raw_word
        # print(raw_word,"sss")
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(raw_word.lower())        
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        # filtered_sentence_word = ""
        filtered_sentence = []
        stop_word_more = ["#","@","!","+","=","_","-",".",",","","'s","An","*","(",")","?","``","''","`","'",".","©","the","an","THE","The","i","I","s","a",'','"','"',"<",">",":","[","]", 'about', 'above', 'across', 'after', 'afterwards', 'again',
        'against', 'all', 'almost', 'alone', 'along', 'already', 'also',
        'although', 'always', 'am', 'among', 'amongst', 'amount', 'an',
        'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway',
        'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became',
        'because', 'become', 'becomes', 'becoming', 'been', 'before',
        'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
        'between', 'beyond', 'both', 'bottom', 'but', 'by', 'call', 'can',
        'cannot', 'could', 'do', 'done', 'down', 'due', 'during', 'each',
        'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty',
        'enough', 'even', 'ever', 'every', 'everyone', 'everything',
        'everywhere', 'except', 'few', 'fifteen', 'fifty', 'first', 'five',
        'for', 'former', 'formerly', 'forty', 'four', 'from', 'front',
        'full', 'further', 'get', 'give', 'go', 'had', 'has', 'have', 'he',
        'hence', 'her', 'here', 'hereafter', 'hereby', 'herein',
        'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how',
        'however', 'hundred', 'i', 'if', 'in', 'indeed', 'into', 'is',
        'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly',
        'least', 'less', 'made', 'many', 'may', 'me', 'meanwhile', 'might',
        'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much',
        'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
        'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone',
        'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often',
        'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others',
        'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
        'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
        'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several',
        'she', 'should', 'show', 'side', 'since', 'six', 'sixty', 'so',
        'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes',
        'somewhere', 'still', 'such', 'take', 'ten', 'than', 'that', 'the',
        'their', 'them', 'themselves', 'then', 'thence', 'there',
        'thereafter', 'thereby', 'therefore', 'therein', 'thereupon',
        'these', 'they', 'third', 'this', 'those', 'though', 'three',
        'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too',
        'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'under',
        'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
        'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where',
        'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon',
        'wherever', 'whether', 'which', 'while', 'whither', 'who',
        'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with',
        'within', 'without', 'would', 'yet', 'you', 'your', 'yours',
        'yourself', 'yourselves',"'",'"','“','’','”',"–"]
        
        stop_word_more.append(str(Keyword))
        ## nlp
        for w in word_tokens:
            if w not in stop_words:        
                if w not in stop_word_more:      
                    # filtered_sentence_word += w +" "     
                    filtered_sentence.append(w)
        # print(filtered_sentence,"fs")
        ##
        ### top word
        N = 10
        words = {}

        words_gen = (wordg.strip(punctuation).lower() for line in filtered_sentence
                                           for wordg in line.split())

        for wordg in words_gen:
            words[wordg] = words.get(wordg, 0) + 1

        top_words = sorted(words.items(), key=itemgetter(1), reverse=True)[:N]
        
        ##
        self.data=[]
        # print(top_words,"top")
        for i, (word, frequency) in enumerate(top_words, start=1):
            self.data.append([i,word,frequency])  
            
        html_text = pd.DataFrame(data=self.data, 
                    columns=["Rank","Word","Frequency"])   
        
        if not os.path.exists(f'./DataRelate'):                    
            os.mkdir(f'./DataRelate')  
            print("CreteFolder Successed")
                 
        open(f"./DataRelate/"+f"{Keyword}"+".csv","w")
        html_text.to_csv(f"./DataRelate/"+f"{Keyword}"+".csv")    
    

    
    def start_scan(self,keyword):
        self.loadfile(keyword)
        word = keyword.lower()
        os.remove(f"./DataKeyword/_{word}.csv")
   

        
        
