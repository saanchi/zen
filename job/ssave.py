from zen.job.models import Corpus

def corpus_save(fscript, title):
    for data in fscript:
        c = Corpus(name=title, 
               source=data['dat'], 
               typ=data['typ']
               )
        c.save()
        
