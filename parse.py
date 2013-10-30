from nltk import pos_tag, word_tokenize
import json,re

app_list = {'evernote','facebook','email'}
c_words = {'if', 'when'}
sent = "send me an email if there's a new facebook post on my wall"
sent = "create a evernote if I received an email from Paul"
tagged = pos_tag(word_tokenize('they '+sent))
del(tagged[0])
print str(tagged)
words = [t[0] for t in tagged]
#find the condition word 'if', 'when' etc
c_indexes = (words.index(word) for word in words if word in c_words)
c_index = c_indexes.next()
#split the sentence
action_phrase = words[:c_index]
condition_phrase = words[c_index+1:]
print 'action_phrase:'
print action_phrase
print 'condition_phrase:'
print condition_phrase
#search valid entities
indexes = [words.index(word) for word in action_phrase if word in app_list]
action_entities = [words[index] for index in indexes]
indexes = [words.index(word) for word in condition_phrase if word in app_list]
condition_entities = [words[index] for index in indexes]
#search for other parameters
verbs = [tagg[0] for tagg in tagged if re.search('VB', tagg[1])]
print 'verbs:', verbs
print 'action entities:'
print str(action_entities)
print 'condition entities:'
print str(condition_entities)


# expected final output:
action = json.dumps(
    {
        'evernote':
        {
            'type': 'evernote',
            'action': 'take_note',
            'condition':
            {
                'type': 'facebook',
                'action': 'post',
                'args': 'on my wall'
            }
        },
        'email':
        {
            'type': 'email',
            'action': 'send',
            'content': 'qu nian mai le ge biao',
            'to' : 'me',
            'condition':
            {
                'type': 'facebook',
                'action': 'post',
                'args': 'on my wall'
            },
        }
    },indent = 4)
#print action
