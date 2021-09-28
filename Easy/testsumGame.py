import hashlib
def testsumGame(function):
  output = ""
  result = str(function(2, 1))
  resultHash = hashlib.md5(result.encode()).hexdigest()
  if resultHash == 'eccbc87e4b5ce2fe28308fd9f2a7baf3':
    output += "Test Case 1: \n" + result + "\n Test PASSED!\n\n"
  else:
    output += "Test Case 1: \n" + result + "\n Test FAILED!\n\n"
  result = str(function(-100, 100))
  resultHash = hashlib.md5(result.encode()).hexdigest()
  if resultHash == 'cfcd208495d565ef66e7dff9f98764da':
    output += "Test Case 2: \n" + result + "\n Test PASSED!\n\n"
  else:
    output += "Test Case 2: \n" + result + "\n Test FAILED!\n\n"
  return output
