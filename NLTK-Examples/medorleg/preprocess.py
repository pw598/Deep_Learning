# -*- coding: utf-8 -*-
from __future__ import division
import glob
import nltk
import re
from xml.dom.minidom import Node
from xml.dom.minidom import parseString

def medical_plaintext(fn):
  print "processing", fn
  if not (fn.startswith("data/medical/eph_") or
      fn.startswith("data/medical/gemd_") or
      fn.startswith("data/medical/gesu_") or
      fn.startswith("data/medical/gea2_") or
      fn.startswith("data/medical/gem_") or
      fn.startswith("data/medical/gech_") or
      fn.startswith("data/medical/geca_") or
      fn.startswith("data/medical/gecd_") or
      fn.startswith("data/medical/gegd_") or
      fn.startswith("data/medical/gend_") or
      fn.startswith("data/medical/gec_") or
      fn.startswith("data/medical/genh_") or
      fn.startswith("data/medical/nwaz_")):
    return ""
  file = open(fn, 'rb')
  data = file.read()
  file.close()
  # remove gale: namespace from attributes
  data = re.sub("gale:", "", data)
  dom = parseString(data)
  text = ""
  paragraphs = dom.getElementsByTagName("p")
  for paragraph in paragraphs:
    xml = paragraph.toxml()
    xml = re.sub("\n", " ", xml)
    xml = re.sub("<.*?>", "", xml)
    text = text + " " + xml
  text = re.sub("\\s+", " ", text)
  text = text.strip()
  text = text.encode("ascii", "ignore")
  return text

def legal_plaintext(fn):
  print "processing", fn
  file = open(fn, 'rb')
  data = file.read()
  data = re.sub("&eacute;", "e", data)
  data = re.sub("&aacute;", "a", data)
  data = re.sub("&yacute;", "y", data)
  data = re.sub("&nbsp;", " ", data)
  data = re.sub("&tm;", "(TM)", data)
  data = re.sub("&reg;", "(R)", data)
  data = re.sub("&agrave;", "a", data)
  data = re.sub("&egrave;", "e", data)
  data = re.sub("&igrave", "i", data)
  data = re.sub("&ecirc;", "e", data)
  data = re.sub("&ocirc;", "o", data)
  data = re.sub("&icirc;", "i", data)
  data = re.sub("&ccedil;", "c", data)
  data = re.sub("&amp;", "and", data)
  data = re.sub("&auml;", "a", data)
  data = re.sub("&szlig;", "ss", data)
  data = re.sub("&aelig;", "e", data)
  data = re.sub("&iuml;", "i", data)
  data = re.sub("&euml;", "e", data)
  data = re.sub("&ouml;", "o", data)
  data = re.sub("&uuml;", "u", data)
  data = re.sub("&acirc;", "a", data)
  data = re.sub("&oslash;", "o", data)
  data = re.sub("&ntilde;", "n", data)
  data = re.sub("&Eacute;", "E", data)
  data = re.sub("&Aring;", "A", data)
  data = re.sub("&Ouml;", "O", data)
  data = re.sub("?", "e", data)
  # fix "id=xxx" pattern, causes XML parsing to fail
  data = re.sub("\"id=", "id=\"", data)
  file.close()
  text = ""
  dom = parseString(data)
  sentencesEl = dom.getElementsByTagName("sentences")[0]
  for sentenceEl in sentencesEl.childNodes:
    if sentenceEl.nodeType == Node.ELEMENT_NODE:
      stext = sentenceEl.firstChild.data
      if len(stext.strip()) == 0:
        continue
      text = text + " " + re.sub("\n", " ", stext)
  text = re.sub("\\s+", " ", text)
  text = text.strip()
  text = text.encode("ascii", "ignore")
  return text

def convert_to_plaintext(dir, ofn, category, func):
  ofile = open(ofn, 'wb')
  files = glob.glob("/".join([dir, "*.xml"]))
  for file in files:
    text = func(file)
    if len(text.strip()) > 0:
      for sentence in nltk.sent_tokenize(text):
        ofile.write("%s\n" % ("|".join([category, sentence])))
  ofile.close()

def main():
  convert_to_plaintext("data/medical", "medical.txt", "M", medical_plaintext)
  convert_to_plaintext("data/legal", "legal.txt", "L", legal_plaintext)

if __name__ == "__main__":
  main()