from nltk import pos_tag, word_tokenize
import json,re
from helpers import refine, wrapped_tagger, wrapped_parse


#define stuff
app_list = {'evernote','facebook','email','text message'}
c_words = {'if', 'when'}
sent = "send an email to Paul if there's a new facebook post on my wall"
sent = """
    create an evernote about yesterday and
    send me an email about it and
    send me a text message
    if
    I received an email from Paul or
    I received a text message
    """
print 'sentence:'
print sent
#pre-processing
print
print 'pre-processing----------------'
print
#refine app_list and sentence for furthur processing
app_list, sent = refine(app_list,sent)
print 'app_list:',app_list
print 'new sentence:', sent
#done refine

tokens = word_tokenize(sent)
#search for conditional words ( 'if', 'when' )
c_indexes = (tokens.index(word) for word in tokens if word in c_words)
c_index = c_indexes.next()
#split into action phrase and condition phrase
a_phrase = tokens[:c_index]
c_phrase = tokens[c_index+1:]
#split due to 'and', 'or' for multiple conditions/actions
a_parts = ' '.join(a_phrase).split(' and ')
c_parts = re.split(' and | or ', ' '.join(c_phrase))
print "a_parts: ", a_parts
print "c_parts: ", c_parts
print
#search valid entities
a_entities = [word for word in app_list if word in a_phrase]
c_entities = [word for word in app_list if word in c_phrase]
entities = set(a_entities+c_entities)
print 'a_entities'
print a_entities
print 'c_entities'
print c_entities
print
print 'end pre_processing -----------'
print

#tagging
print 'tagging-----------------------'
print
a_tagged_list = wrapped_tagger(a_parts)
c_tagged_list = wrapped_tagger(c_parts)
print
print 'done tagging -----------------'
print
print 'parsing-----------------------'
print
for a_tagged in a_tagged_list:
    a_verb, a_entity, a_params = wrapped_parse(a_tagged, entities)
for c_tagged in c_tagged_list:
    c_verb, c_entity, c_params = wrapped_parse(c_tagged, entities)
print 'a_list:', a_verb
print 'c_list:', c_verb
print
print 'done parsing-----------------'
#result = {'action':
#          {
#              'entities': a_entities,
#              'verb': a_verbs,
#              'params': a_params,
#          },
#          'condition':
#          {
#              'entities' : c_entities,
#              'verb': c_verbs,
#              'params': c_params
#          }}
#print 'result:'
#print json.dumps(result,indent = 4)


# expected final output:
#action = json.dumps(
#    {
#        'evernote':
#        {
#            'type': 'evernote',
#            'action': 'take_note',
#            'condition':
#            {
#                'type': 'facebook',
#                'action': 'post',
#                'args': 'on my wall'
#            }
#        },
#        'email':
#        {
#            'type': 'email',
#            'action': 'send',
#            'content': 'qu nian mai le ge biao',
#            'to' : 'me',
#            'condition':
#            {
#                'type': 'facebook',
#                'action': 'post',
#                'args': 'on my wall'
#            },
#        }
#    },indent = 4)
#print action
