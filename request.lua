wrk.method = "POST"
wrk.body = "{\"test_array\": '[0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,1,1,0,1,0,1,0]'}"
wrk.headers["Content-Type"] = "application/json"