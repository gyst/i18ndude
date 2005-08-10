import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from utils import PACKAGE_HOME

try:
    from Products.i18ndude import catalog
except ImportError:
    from i18ndude import catalog

class TestGlobal(ZopeTestCase.ZopeTestCase):

    def test_isLiteralId(self):
        i = catalog.is_literal_id
        errortext = 'False literal msgid recognition'
        self.failIf(i('label_yes'), errortext)
        self.failIf(i('_'), errortext)
        self.failUnless(i(' '), errortext)
        self.failUnless(i(' _'), errortext)
        self.failUnless(i('text'), errortext)
        self.failUnless(i('This is a text.'), errortext)

    def test_originalComment(self):
        self.assertEquals(catalog.ORIGINAL_COMMENT, 'Original: ', 'Wrong original comment constant')


class TestMessageCatalogInit(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        self.mc = catalog.MessageCatalog
        self.file = os.path.join(PACKAGE_HOME, 'input', 'test-en.po')
        self.emptyfile = os.path.join(PACKAGE_HOME, 'input', 'empty-en.po')

        self.commentary_header = ['Translation of test.pot to English', 'Hanno Schlichting <schlichting@bakb.net>, 2005']

        self.mimeheader = {'Language-Code': 'en', 'Domain': 'testing', 'PO-Revision-Date': '2005-08-10 21:15+0000', 'Content-Transfer-Encoding': '8bit',
                           'Language-Name': 'English', 'X-Is-Fallback-For': 'en-au en-bz en-ca en-ie en-jm en-nz en-ph en-za en-tt en-gb en-us en-zw',
                           'Plural-Forms': 'nplurals=1; plural=0;', 'Project-Id-Version': 'i18ndude', 'Preferred-Encodings': 'utf-8 latin1',
                           'Last-Translator': 'Unic\xf6d\xe9 Guy', 'Language-Team': 'Plone i18n <plone-i18n@lists.sourceforge.net>',
                           'POT-Creation-Date': '2005-08-01 12:00+0000', 'Content-Type': 'text/plain; charset=utf-8', 'MIME-Version': '1.0'
                          }

        self.nocomments = {'msgid1' : ('msgstr1', [('file2', ['excerpt2', 'excerpt3']), ('file1', ['excerpt1'])], ['comment1', 'Original: "msgstr1"']),
                           'msgid2' : ('msgstr2', [('file2', ['excerpt2'])], []),
                           'msgid3' : ('msgstr3', [('file3', [])], ['comment3']),
                           'msgid4' : ('msgstr4', [('file4', [])], []),
                           'msgid5' : ('msgstr5', [], ['comment5']),
                           'msgid6' : ('msgstr6', [], []),
                           'msgid has spaces' : ('msgstr has spaces', [], []),
                           'msgid_has_underlines' : ('msgstr_has_underlines', [], []),
                           'msgid_has_underlines and spaces' : ('msgstr_has_underlines and spaces', [], []),
                           'msgid for unicode text' : ('unicode msgstr \xb7\xb7\xb7', [], []),
                           'msgid for unicode text with comment' : ('unicode msgstr \xb7\xb7\xb7', [('./folder/file_unicode', ['unicode \xb7\xb7\xb7 excerpt'])], ['Original: [\xb7\xb7\xb7]']),
                           'msgid for text with german umlaut' : ('\xe4\xf6\xfc\xdf text', [], []),
                           'msgid for text with html-entity' : ('&quot;this&nbsp;is&laquo;&auml;&amp;&ouml;&raquo;&quot;', [], [])
                          }

        self.allcomments = {'msgid1' : ('msgstr1', [('file2', ['excerpt2', 'excerpt3']), ('file1', ['excerpt1'])], ['comment1', 'Original: "msgstr1"']),
                            'msgid2' : ('msgstr2', [('file2', ['excerpt2'])], []),
                            'msgid3' : ('msgstr3', [('file3', [])], ['comment3']),
                            'msgid4' : ('msgstr4', [('file4', [])], []),
                            'msgid5' : ('msgstr5', [], ['comment5']),
                            'msgid6' : ('msgstr6', [], []),
                            'msgid has spaces' : ('msgstr has spaces', [], []),
                            'msgid_has_underlines' : ('msgstr_has_underlines', [], []),
                            'msgid_has_underlines and spaces' : ('msgstr_has_underlines and spaces', [], []),
                            'msgid for unicode text' : ('unicode msgstr \xb7\xb7\xb7', [], []),
                            'msgid for unicode text with comment' : ('unicode msgstr \xb7\xb7\xb7', [('./folder/file_unicode', ['unicode \xb7\xb7\xb7 excerpt'])], ['Original: [\xb7\xb7\xb7]']),
                            'msgid for text with german umlaut' : ('\xe4\xf6\xfc\xdf text', [], []),
                            'msgid for text with html-entity' : ('&quot;this&nbsp;is&laquo;&auml;&amp;&ouml;&raquo;&quot;', [], [])
                           }

    def test_init(self):
        failing = False
        try:
            test = catalog.MessageCatalog()
        except AssertionError:
            failing = True
        self.failUnless(failing, 'Init without parameters should not be allowed.')

    def test_initWithDomain(self):
        domain = 'testing'
        test = self.mc(domain=domain)
        mime = catalog.DEFAULT_PO_MIME
        for key,value in mime:
            if key != 'Domain':
                self.assertEquals(value, test.mime_header[key], 'header mismatch on %s' % key)
            else:
                self.assertEquals(domain, test.mime_header['Domain'], 'Domain mismatch')
        self.assertEquals(catalog.DEFAULT_PO_HEADER, test.commentary_header, 'commentary header mismatch')
        self.assertEquals(len(test), 0, 'Non-empty catalog')

    def test_initWithEmptyFile(self):
        test = self.mc(filename=self.emptyfile)
        mime = catalog.DEFAULT_PO_MIME
        for key,value in mime:
            self.assertEquals(value, test.mime_header[key], 'header mismatch on %s' % key)

    def test_initWithEmptyFileAndDomain(self):
        failing = False
        try:
            test = self.mc(domain='testing', filename=self.emptyfile)
        except AssertionError:
            failing = True
        self.failUnless(failing, 'Init with filename and domain parameters is not allowed.')

    def test_initWithFile(self):
        test = self.mc(filename=self.file)
        for key in test.mime_header:
            self.assertEquals(test.mime_header[key], self.mimeheader[key], 'wrong mime header parsing')
        for value in test.commentary_header:
            self.failUnless(value in self.commentary_header, 'wrong commentary header parsing')
        if not test == self.nocomments:
            for key in test:
                self.assertEquals(test[key], self.nocomments[key], 'error in po parsing:\n Got: %s !=\nExpected: %s' % (test[key], self.nocomments[key]))

    def test_initWithFileAllComments(self):
        test = self.mc(filename=self.file, allcomments=True)
        for key in test.mime_header:
            self.assertEquals(test.mime_header[key], self.mimeheader[key], 'wrong mime header parsing')
        for value in test.commentary_header:
            self.failUnless(value in self.commentary_header, 'wrong commentary header parsing')
        if not test == self.allcomments:
            for key in test:
                self.assertEquals(test[key], self.allcomments[key], 'error in po parsing:\n Got: %s !=\nExpected: %s' % (test[key], self.allcomments[key]))

class TestMessageCatalog(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        self.domain = 'testing'
        self.mc = catalog.MessageCatalog(domain=self.domain)
        self.msgid = 'test msgid'
        self.msgstr = 'test text'
        self.filename = 'test.pt'
        self.excerpt = ['first line', 'second line']
        self.excerpt2 = ['first line2', 'second line2']
        self.orig_text = 'test original'
        self.orig_comment = '%s"%s"' % (catalog.ORIGINAL_COMMENT, self.orig_text)
        self.comment = ['A comment', self.orig_comment]

    def test_add(self):
        msgid = self.msgid
        msgstr = self.msgstr
        filename = self.filename
        excerpt = self.excerpt

        # add with msgid
        self.mc.add(msgid)
        self.failUnless(msgid in self.mc, 'msgid not found in catalog')
        del self.mc[msgid]
        self.failIf(msgid in self.mc, 'msgid found in catalog')
        # add with msgid and msgstr
        self.mc.add(msgid, msgstr=msgstr)
        self.assertEquals(self.mc[msgid][0], msgstr, 'msgstr not found in catalog.')
        del self.mc[msgid]
        self.failIf(msgid in self.mc, 'msgid found in catalog')
        # add with msgid, msgstr and filename
        self.mc.add(msgid, msgstr=msgstr, filename=filename)
        self.assertEquals(self.mc[msgid][1][0][0], filename, 'filename not found in catalog.')
        del self.mc[msgid]
        self.failIf(msgid in self.mc, 'msgid found in catalog')
        # add with msgid, msgstr, filename and excerpt
        self.mc.add(msgid, msgstr=msgstr, filename=filename, excerpt=excerpt)
        self.assertEquals(self.mc[msgid][1][0][1], excerpt, 'excerpt not found in catalog.')
        del self.mc[msgid]
        self.failIf(msgid in self.mc, 'msgid found in catalog')

    def test_multipleAdd(self):
        msgid = self.msgid
        msgstr = self.msgstr
        filename = self.filename
        excerpt = self.excerpt
        excerpt2 = self.excerpt2
        
        self.mc.add(msgid, msgstr=msgstr, filename=filename, excerpt=excerpt)
        self.mc.add(msgid, msgstr=msgstr, filename=filename, excerpt=excerpt)
        self.failUnless(len(self.mc)==1, 'duplicate msgid')
        self.failUnless(len(self.mc[msgid][1])==2, 'second occurrence missing')
        self.mc.addToSameFileName(msgid, msgstr=msgstr, filename=filename, excerpt=excerpt)
        self.failUnless(len(self.mc[msgid][1][1][1])==2, 'duplicate occurrence')
        self.mc.addToSameFileName(msgid, msgstr=msgstr, filename=filename, excerpt=excerpt2)
        self.failUnless(len(self.mc[msgid][1][1][1])==4, 'new occurrence missing')

    def test_originalComment(self):
        self.mc.add(self.msgid, msgstr=self.msgstr, filename=self.filename, excerpt=self.excerpt)
        self.mc[self.msgid][2].extend(self.comment)
        self.assertEquals(self.mc.get_comment(self.msgid), self.comment, 'wrong comment')
        self.assertEquals(self.mc.get_original_comment(self.msgid), self.orig_comment, 'wrong original comment line')
        self.assertEquals(self.mc.get_original(self.msgid), self.orig_text, 'wrong original comment text')

class TestMessagePoWriter(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        mc = catalog.MessageCatalog
        self.input = os.path.join(PACKAGE_HOME, 'input', 'test-en.po')
        self.output = os.path.join(PACKAGE_HOME, 'output', 'test-en.po')
        self.catalog = mc(filename=self.input)

    def test_write(self):
        fd = open(self.output, 'wb')
        pow = catalog.POWriter(fd, self.catalog)
        pow.write(sort=True)
        fd.close()

        input = open(self.input, 'r')
        output = open(self.output, 'r')

        # compare line by line
        inlines = input.readlines()
        outlines = enumerate(output.readlines())

        input.close()
        output.close()

        for i, result in outlines:
            orig = inlines[i]
            self.failUnlessEqual(orig, result, 'difference in line %s, \'%s\' != \'%s\'' % (i, orig, result))

    def tearDown(self):
        if os.path.exists(self.output):

            os.remove(self.output)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGlobal))
    suite.addTest(makeSuite(TestMessageCatalogInit))
    suite.addTest(makeSuite(TestMessageCatalog))
    suite.addTest(makeSuite(TestMessagePoWriter))
    return suite

if __name__ == '__main__':
    framework()