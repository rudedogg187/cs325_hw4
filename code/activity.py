import mergesort
import cleanup

#ref pg421 CLRS Text




##################
# Fetch raw data from text file
# Splits data into rows on linebreaks
# Appends flag to end of file to denote file's last row
# Returns file data 
##################
def dataFromFile(name):
  with open("./{}.txt".format(name), "r") as f:
    data = f.read().replace('\r', '')
    data = data.split('\n')
    data.append('XXX')
    return data


##################
# Recursivly turns activity string '1 2 3' into lst [1, 2, 3]
# Returns activitySet 
##################
def splitActivitySet(i, activitySet):
  if i >= len(activitySet):
    return activitySet

  else:
    activitySet[i] = activitySet[i].split(" ")
    i += 1
    return splitActivitySet(i, activitySet)

##################
# Recursivly goes through each activity set
# Looks for empty row and/or file term. flag to end
# Calls spitActivitySet() to turn activity string to lst
# Calls greedyActivitySelector() to select optimal activities
##################
def processActivitySet(i, set_num, data):
  # Base Case - at end of file
  if data[i] == "XXX" or data[i] == '':
    return 

  # Process Activity
  else:
    # get activity set from data
    activitySet = data[i + 1: i + int(data[i]) + 1 ]
    # call to turn activiy parm string into lst of params
    activitySet = splitActivitySet(0, activitySet)

    # call to get greedy activity choice
    result = greedyActivitySelector(activitySet)
    printResult(set_num, result)

    # increment i to the next set of activities in file
    i += int(data[i]) + 1
    set_num += 1

    # call self to process the next activity set
    processActivitySet(i, set_num, data)


##################
##################
def greedyActivitySelector(S, on_fin = False):
  # set k so that is index of element 1 in activities
  k = 0
  # set n to the lenght of activites
  n = len(S)

  # if choosing based on finish time
  if on_fin:
    # call to sort activity set on finish time (index 2)
    mergesort.mergeSortIndex(S, 0, len(S) -1, 2)
    A = [str(S[k][0])]
    for m in range(k, n):
      if int(S[m][1]) >= int(S[k][2]):
        A.append(str(S[m][0]))
        k = m

  # if choosing based on start time
  else:
    # sort so the activites are in desc order of finish time
    mergesort.mergeSortIndex(S, 0, len(S) -1, 2, 1)
    # sort again so that activities are in desc order of start tiem
    mergesort.mergeSortIndex(S, 0, len(S) -1, 1, 1)

    # init lst w/ first activity (activity w/ latest start time)
    A = [str(S[k][0])]
    # iterate through activities from second element
    for m in range(1, n):
      # compare fin time of curr ele to start time of prev ele 
      # if this act is finished before prev act starts
      if int(S[m][2]) <= int(S[k][1]):
        # append the activity id to lst of optimal activites
        A.append(str(S[m][0]))
        # set k to m
        k = m

  # return the lst of optimal activites
  return A


def printResult(set_num, result):
  # sort lst in order of activity name
  mergesort.mergeSort(result, 0, len(result) -1)
  # print result to console
  output = "  Set {}\n".format(set_num)
  output += "  Number of activities selected = {}\n".format(len(result))
  output += "  Activities: {}\n".format(" ".join(result))

  print output


##################
# Test function
# Tests Book's example starting w/ first to finish
##################
def test():
  activitySet = [
    [1, 1, 4], 
    [2, 3, 5], 
    [3, 0, 6],
    [4, 5, 7],
    [5, 3, 9],
    [6, 5, 9],
    [7, 6, 10],
    [8, 8, 11], 
    [9, 8, 12], 
    [10, 2, 14],
    [11, 12, 16]
  ]

  result = greedyActivitySelector(activitySet)
  printResult(1, result)
  cleanup.pyc()


##################
# Test function 2
# Using last to start
# Test's Set 2 in act.txt
##################
def test2():
  S = [
    ['1', '7', '9'], 
    ['3', '6', '8'], 
    ['2', '1', '2']
  ]

  result = greedyActivitySelector(S)
  printResult(1, result)
  cleanup.pyc()




##################
# Main function
# Calls to parse data from file
# Processes each activity in file
# Cleans working directory of compiled py files
##################
def main():
  data = dataFromFile("act")
  processActivitySet(0, 1, data)
  cleanup.pyc()




if __name__ == "__main__":
  main()
















