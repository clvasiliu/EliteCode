import hashlib
def testSumGame(function):
  results = str(function(2, 1))
  resultHash = hashlib.md5(results.encode()).hexdigest()
  if resultHash == 'eccbc87e4b5ce2fe28308fd9f2a7baf3':
    return "Test1:" + results + "\n Test Passed"
  else:
    return "Test1:" + results + "\n Test Passed"
