from django.test import TestCase
from models import Entry
import lexer, models

doctest_modules = [lexer, models]


class EntryTest(TestCase):
    one = lambda self: Entry.objects.get(slug='one')
    two = lambda self: Entry.objects.get(slug='two')
    three = lambda self: Entry.objects.get(slug='three')

    def make_one(self):
        Entry.objects.create(slug='one', name='one', content='{2}(two) {3}(three) {2}(two)').save()

    def all(self):
        self.make_one()
        return self.one(), self.two(), self.three()

    def test_create_stubs(self):
        self.failUnlessRaises(Entry.DoesNotExist, self.one)
        self.failUnlessRaises(Entry.DoesNotExist, self.two)
        self.failUnlessRaises(Entry.DoesNotExist, self.three)
        self.make_one()
        self.one()
        self.two()
        self.three()

    def test_outgoing(self):
        one, two, three = self.all()

        self.failUnless(two in one.outgoing.all())
        self.failUnless(three in one.outgoing.all())

        self.failIf(one in two.outgoing.all())
        self.failIf(three in two.outgoing.all())

        self.failIf(one in three.outgoing.all())
        self.failIf(two in three.outgoing.all())

    def test_incoming(self):
        one, two, three = self.all()

        self.failIf(two in one.incoming.all())
        self.failIf(three in one.incoming.all())

        self.failUnless(one in two.incoming.all())
        self.failIf(three in two.incoming.all())

        self.failUnless(one in three.incoming.all())
        self.failIf(two in three.incoming.all())
