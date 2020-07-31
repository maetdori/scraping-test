import send_email
def check(sitetype, dict, attach_img=None, to=[], cc=[], bcc=[]):

    if attach_img != None:
        return send_email.send(sitetype, dict, attach_img)
    if str(dict) == "{}":
        return sitetype + "\n"
    elif str(dict) == "[]":
        return sitetype + "\n"
    else:
        return send_email.send(sitetype, dict, attach_img)