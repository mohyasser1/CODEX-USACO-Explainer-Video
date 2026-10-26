"""Parse whole-line visual directions without confusing array-index brackets."""
def scenes(raw):
    result=[];cue=[];speech=[];inside=False
    for line in raw[raw.index('['):].splitlines():
        if line.startswith('['):
            assert not inside, 'new direction before previous direction closed'
            if cue: result.append((' '.join(cue),' '.join(speech)))
            cue=[line];speech=[];inside=not line.rstrip().endswith(']')
        elif inside:
            cue.append(line);inside=not line.rstrip().endswith(']')
        else:
            speech.append(line)
    assert not inside, 'unclosed visual direction'
    if cue:result.append((' '.join(cue),' '.join(speech)))
    return result

def narration(raw):
    return ' '.join(speech for _,speech in scenes(raw))
