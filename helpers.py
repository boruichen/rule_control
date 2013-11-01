import re
from nltk import pos_tag, word_tokenize
def refine(app_list, sent):
    """
    this function change possible entities with multiple words into one word
    for example: 'text message' -> 'textmessage'
    """
    for name in app_list:
        if ' ' in name:
            new_name = name.replace(' ','') #'text message'=>'textmessage'
            app_list.remove(name)
            app_list.add(new_name)
            match = re.search(name,sent)
            if match:
                sent = sent.replace(name,new_name)
    return app_list, sent

def wrapped_tagger(parts, _type = 'action'):
    tagged_list = []
    if _type not in ['action','conditon']:
        print 'Warning: invalid type when calling wrapped_tagger'
        _type = 'action'
    if _type == 'action':
        for part in parts:
            part = 'they '+ part
            tokens = word_tokenize(part)
            tagged = pos_tag(tokens)
            del(tagged[0])
            tagged_list.append(tagged)
    elif _type == 'condition':
        for part in parts:
            tokens = word_tokenize(part)
            tagged = pos_tag(tokens)
            tagged_list.append(tagged)
    return tagged_list

def wrapped_parse(tagged, entities):
    words = [t[0] for t in tagged]
    #search for entity
    entity = [word for word in entities if word in words]
    #search for verbs
    verb = [tagg[0] for tagg in tagged if re.search('VB', tagg[1])]
    #search for other parameters
    #get rid of junk words
    params = [tagg[0] for tagg in tagged if isnt_junk(tagg,entities)]
    return verb, entity, params

def isnt_junk(tagg, entities):
    feature_result = False
    redund_result = False
    if not tagg[0] in entities:
        redund_result = True
    for feature in ['NN','TO','PRP','IN']:
        if re.search(feature,tagg[1]):
            feature_result = True
    result = redund_result and feature_result
    return result
