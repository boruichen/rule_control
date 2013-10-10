from pattern.en import Sentence, parse, modality
import re, json

SW_NAME = r'jarvis'

def command_handler(S):
    """ This function takes a Sentence object as parameter
        output the action as json
    """
    for i, word in enumerate(S):
        if word.type == "MD":
            if S[i+1].type == "PRP":
                continue

    return json.dumps({'type': 'command', 'action': 'w/e'}, indent = 4)

def rule_handler(S):
    return json.dumps({'type': 'add rule', 'action': 'w/e'}, indent = 4)

def question_handler(S):
    return json.dumps({'type': 'question', 'action': 'w/e'}, indent = 4)

def error_handler():
    return json.dumps({'type':'error'})

def parse_command(sentence):
    """ This function takes an input sentence as string, parse it and
        output command in json format
    """
    #get rid of 'jarvis'
    match = re.search(r'^.*'+SW_NAME+r'\W*', sentence, flags = re.IGNORECASE)
    print sentence
    if match:
        sentence = re.sub(match.group(), '', sentence, re.IGNORECASE)
    print sentence
    #parse
    S = Sentence(parse(sentence))
    chunks = S.chunks
    for i, word in enumerate(S):
        w = word.string.lower()
        if w in ['when', 'while']:
            if not word.chunk or word.chunk.next() == None:
                print "'when','while' should not be at end of sentence"
                print "unexpected error"
                return error_handler()
            else:
                if word.chunk.next().type == 'NP':
                    #this is a conditional command
                    return rule_handler(S)
                else:
                    #this is a question
                    return question_handler(S)
        elif w in ['what', 'while', 'why', 'how', 'who', 'whose', 'where']:
            #this is a question
            return question_handler(S)
        elif w in ['if', 'as', 'after', 'before', 'since', 'till', 'until',
                   'whenever','unless']:
            #this is a conditional command
            return rule_handler(S)
    if S.words[0].chunk.type == 'VP':
        return command_handler(S)
    return 'idk'

if __name__ == '__main__':
    print
    print parse_command('Jarvis, could you turn on the light')
    print
    print parse_command('jarvis please open the door')
    print
    print parse_command("yo jarvis, please turn on the light when I'm not at home")
    print
    print parse_command("yo jarvis, turn on the light when I'm not at home")
    print
    print parse_command("when the door bell rang, send me a text message")
    print
    print parse_command("wo qu nian mai le ge biao jarvis, make sure the light is off till tommorow 8am")
    print parse_command("wo make sure while")
