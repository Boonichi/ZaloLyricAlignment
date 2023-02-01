from ..libs import*
from ..postprocessing.forced_alignment import(
    get_trellis,
    backtrack,
    merge_repeats,
    merge_words 
)

from ..data_pipeline.demus import(
    get_denoiser,
    run_denoiser,
)

special_characters = {"ð" : "đ"}
labels=("ẻ","6","ụ","í","3","ỹ","ý","ẩ","ở","ề","õ","7","ê","ứ","ỏ","v","ỷ","a","l","ự","q","ờ","j","ố","à","ỗ","n","é","ủ","у","ô","u","y","ằ","4","w","b","ệ","ễ","s","ì","ầ","ỵ","8","d","ể","|","r","ũ","c","ạ","9","ế","ù","ỡ","2","t","i","g","́ ","ử","̀ ","á","0","ậ","e","ộ","m","ẳ","ợ","ĩ","h","â","ú","ọ","ồ","ặ","f","ữ","ắ","ỳ","x","ó","ã","ổ","ị","̣ ","z","ả","đ","è","ừ","ò","ẵ","1","ơ","k","ẫ","p","ấ","ẽ","ỉ","ớ","ẹ","ă","o","ư","5","<","<pad>")
dictionary = {c: i for i, c in enumerate(labels)}

class Lyrics_to_alignment():
    def __init__(self, vocal_path, lyric,get_lyric_function=None):
        self.vocal_path         = vocal_path
        self.lyric              = lyric
        self.processor          = Wav2Vec2Processor.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")
        self.model              = Wav2Vec2ForCTC.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")
        self.denoiser           = get_denoiser(device)
        self.get_lyric_function = get_lyric_function

    def denoise_data(self):
        data,_=run_denoiser(self.denoiser,self.vocal_path)
        return data

    def downsample(self, vocal, original_sr=44100, targ_sr = 16000):
        lowSignal = librosa.resample(vocal, orig_sr=original_sr, target_sr=targ_sr)
        return lowSignal
    
    def get_lyric(self):
        if(self.get_lyric_function==None):
            return self.lyric
        
        return self.get_lyric_function(self.lyric)
    
    def preprocessing(self,lyric):
        
        if not type(lyric) is list:
            if self.get_lyric_function == None:
                raise TypeError('lyric must be in list type')
            else:
                raise TypeError('get_lyric_function must return list type')
            
    
        lyrics=[]
        for word in lyric:
            word=word.replace(',','')
            word=word.replace('.','')            
            #some special case of sign có thể đọc thành 2 âm tiết
            if("’" in word):
                #some special case other we keep the same 
                if("re" in word):
                    word=word.replace("re","are")
                if("s" in word):
                    word=word.replace("s","is")
                if("ll" in word):
                    word=word.replace("ll","will")
                word=word.replace("’","|")
            if ("$" in word):
                word=word.replace("$","|$")
                    
            if("%" in word):
                word=word.replace('%',"|%")
                    
            if("@" in word):
                word=word.replace("@","|@|")
                
            if(word[-1]=="|"): 
                word=word[:-1]
                
            lyrics.append(word)
        lyrics = "|".join(lyrics).lower()            
            
        res = ""
        for e in lyrics:
            if (e in special_characters):
                res += special_characters[e]
            elif (e == "|" or e.isalnum()):
                res+=e
            else :
                res+="|"
        return res
    
    def Wav2Vec(self,vocal):
        input_values = self.processor(vocal, return_tensors="pt", padding="longest", sampling_rate = 16000).input_values  # Batch size 1

        # retrieve logits
        logits = self.model(input_values).logits

        emission=torch.log_softmax(logits,dim=-1)[0].cpu().detach()
        return emission
    
    def run(self):
        vocal       = self.denoise_data() 
        vocal       = self.downsample(vocal)
        lyric       = self.get_lyric()
        lyric       = self.preprocessing(lyric)
        emission    = self.Wav2Vec(vocal)
        tokens      = [dictionary[c] for c in lyric]
        trellis     = get_trellis(emission, tokens)
        path        = backtrack(trellis,emission, tokens)
        segments    = merge_repeats(path, lyric)
        words       = merge_words(segments)
        return words, trellis.shape[0],vocal
        
        
    
    
    
    

    

