import requests as r
import re
import urllib
import urllib2
import sys

def get_page(url):
    html = r.get(url)
    return html

def downloader(fileurl,file_name):
    u = urllib2.urlopen(fileurl)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "[Drama Crazy]  Downloading %s (%s bytes)" %(file_name, file_size)
    file_size_dl = 0
    block_size = 8192

    #Download loop
    while True:
        buffer = u.read(block_size)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = "%s [%3.2f%%]" % (convertSize(file_size_dl), file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        #print status
        sys.stdout.write("\r  \r      %s" % status)
        sys.stdout.flush()

    #Download done. Close file stream
    f.close()


def convertSize(n, format='%(value).1f %(symbol)s', symbols='customary'):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",
    see: http://goo.gl/kTQMs
    """
    SYMBOLS = {
    'customary'     : ('B', 'K', 'Mb', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                       'zetta', 'iotta'),
    'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                       'zebi', 'yobi'),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


try:
    if len(sys.argv) >1:
        first_url = sys.argv[1]
    else:
        first_url = raw_input("[Drama Crazy] What is the url?\t")

    html = get_page(first_url)
    print "[Drama Crazy] Extracting information"
    file_name = html.url.split('/')[-1].split('.')[0] + ".mp4"
    second_url = urllib.unquote("http://www.dramacrazy.co/" +re.search(r'<iframe src="(.+?)"',html.text).group(1)[9:])
    html = get_page(second_url)
    third_url = re.search(r'src="(.+?)"',html.text).group(1)
    html = get_page(third_url)
    base_url = '/'.join(urllib.unquote(html.url).split('/')[:3])
    final_url = base_url + urllib.unquote(re.search(r'fpath=(.+?)&',html.text).group(1))
    downloader(final_url, file_name)

except KeyboardInterrupt:
    print "\r[Drama Crazy] Program was terminated by user"
