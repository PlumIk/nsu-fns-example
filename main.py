import json
from for_nalog.nalog_python import NalogRuPython



def request_to_fns(qr_code):
    client = NalogRuPython()
    ticket = client.get_ticket(qr_code)
    answer = str(json.dumps(ticket, indent=4, ensure_ascii=False))
    return answer


if __name__ == '__main__':
    qr_code = 't=20210506T153900&s=263.50&fn=9960440300049147&i=36086&fp=3305237468&n=1'
    res = request_to_fns(qr_code)
    print(res)

    with open('bill.json', "w", encoding="utf-8") as f:
        f.write(res)
        f.close()