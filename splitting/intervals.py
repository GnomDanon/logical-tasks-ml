def createIntervalsTopics(topicsIdxs,lenTxt):
  res = []
  for i in topicsIdxs:
    res.append(i[1])
  res.append(lenTxt)
  return [(res[i],res[i+1]) for i in range(len(res)-1)]

def getRequiredParagraphs(idxs,txt,intervals):
  return [txt[intervals[i][0]:intervals[i][1]] for i in idxs]

