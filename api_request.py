#!/usr/bin/python

import sys
import os
import base64
import requests

def generateMultipartBody(xmlContent, imageFile, boundary, cidPrefix):
    CRLF = '\r\n'
    newLine = ''
    boundary = '--%s' % boundary

    # Get the binary image content
    filename = os.path.basename(imageFile)
    fileContent = open(filename, "rb").read()

    bodyLines = []

    # Append xml to the body
    bodyLines.append(boundary)
    bodyLines.append('Content-type: application/xml; charset=utf-8')
    bodyLines.append(newLine)
    bodyLines.append(xmlContent)

    # Append file to the body
    bodyLines.append(boundary)
    bodyLines.append('Content-Type: image/png')
    bodyLines.append('Content-Disposition: attachment; filename="%s"' % filename)
    bodyLines.append('Content-ID: <%s>' % cidPrefix)
    bodyLines.append(newLine)
    bodyLines.append(fileContent)
    bodyLines.append(newLine)
    bodyLines.append(boundary)
    bodyLines.append(newLine)

    return CRLF.join(bodyLines)

def extractXmlFromFile(filename):
    try:
        return open(filename, "r").read()
    except IOError as e:
        print 'Error reading the xml file at: %s' % (filename)
        sys.exit(1)

def makeApiRequest(url, headers, body):
    session = requests.session()
    response = session.post(
        url,
        headers=headers,
        data=body,
        verify=False
    )
    return response

xmlFile  = 'receipt.create.xml'
imageFile  = 'image.png'
authenticationToken = ''

subdomain = ''
url = 'https://%s/api/2.1/xml-in' % subdomain

boundary = 'MYBOUNDARY'
cidPrefix = 'imagefile'

xmlRequest = extractXmlFromFile(xmlFile)
body = generateMultipartBody(xmlRequest, imageFile, boundary, cidPrefix)

headers = {
    'Content-Type': 'multipart/related; boundary="%s"' % boundary,
    'Content-Length': str(len(body)),
    'authorization' : "Basic %s" % base64.b64encode("%s:" % (authenticationToken))
}

response = makeApiRequest(url, headers, body)
print response.headers
print response.content
