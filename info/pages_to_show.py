from django.core.paginator import Paginator
import unittest

class Pages:

    def __init__(self, objects, count):
        self.pages = Paginator(objects, count)

    def pages_to_show(self, page):
        # pages_wanted stores the pages we want to see, e.g.
        #  - first and second page always
        #  - two pages before selected page
        #  - the selected page
        #  - two pages after selected page
        #  - last two pages always
        #
        # Turning the pages into a set removes duplicates for edge
        # cases where the "context pages" (before and after the
        # selected) overlap with the "always show" pages.
        pages_wanted = set([1,2,
                            page-2, page-1,
                            page,
                            page+1, page+2,
                            self.pages.num_pages-1, self.pages.num_pages])

        # The intersection with the page_range trims off the invalid
        # pages outside the total number of pages we actually have.
        # Note that includes invalid negative and >page_range "context
        # pages" which we added above.
        pages_to_show = set(self.pages.page_range).intersection(pages_wanted)
        pages_to_show = sorted(pages_to_show)

        # skip_pages will keep a list of page numbers from
        # pages_to_show that should have a skip-marker inserted
        # after them.  For flexibility this is done by looking for
        # anywhere in the list that doesn't increment by 1 over the
        # last entry.
        skip_pages = [ x[1] for x in zip(pages_to_show[:-1],
                                         pages_to_show[1:])
                       if (x[1] - x[0] != 1) ]

        # Each page in skip_pages should be follwed by a skip-marker
        # sentinel (e.g. -1).
        for i in skip_pages:
            pages_to_show.insert(pages_to_show.index(i), -1)

        return pages_to_show

class TestPages(unittest.TestCase):

    def runTest(self):

        objects = [x for x in range(0,1000)]
        p = Pages(objects, 10)

        self.assertEqual(p.pages_to_show(0),
                         [1, 2, -1, 99, 100])
        self.assertEqual(p.pages_to_show(1),
                         [1,2,3,-1,99,100])
        self.assertEqual(p.pages_to_show(2),
                         [1,2,3,4,-1,99,100])
        self.assertEqual(p.pages_to_show(3),
                         [1,2,3,4,5,-1,99,100])
        self.assertEqual(p.pages_to_show(4),
                         [1,2,3,4,5,6,-1,99,100])
        self.assertEqual(p.pages_to_show(5),
                         [1,2,3,4,5,6,7,-1,99,100])
        self.assertEqual(p.pages_to_show(6),
                         [1,2,-1,4,5,6,7,8,-1,99,100])
        self.assertEqual(p.pages_to_show(7),
                         [1,2,-1,5,6,7,8,9,-1,99,100])

        self.assertEqual(p.pages_to_show(50),
                         [1,2,-1,48,49,50,51,52,-1,99,100])

        self.assertEqual(p.pages_to_show(93),
                         [1,2,-1,91,92,93,94,95,-1,99,100])
        self.assertEqual(p.pages_to_show(94),
                         [1,2,-1,92,93,94,95,96,-1,99,100])
        self.assertEqual(p.pages_to_show(95),
                         [1,2,-1,93,94,95,96,97,-1,99,100])
        self.assertEqual(p.pages_to_show(96),
                         [1,2,-1,94,95,96,97,98,99,100])
        self.assertEqual(p.pages_to_show(97),
                         [1,2,-1,95,96,97,98,99,100])
        self.assertEqual(p.pages_to_show(98),
                         [1,2,-1,96,97,98,99,100])
        self.assertEqual(p.pages_to_show(99),
                         [1,2,-1,97,98,99,100])
        self.assertEqual(p.pages_to_show(100),
                         [1,2,-1,98,99,100])


if __name__ == '__main__':
    unittest.main()