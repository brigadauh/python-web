def responseOK():
    return '{"status":1}'

def responseErr(err, err_message):
    return'{"status":0,"err":"'+err+'","message":"'+err_message+'"}'