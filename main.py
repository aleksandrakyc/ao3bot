import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

# this is dumb, make a list of dicts
# possible features:
# - adding to a query: language, excluding stuff
# - make this run at a realistic speed
# - save a number of fics relative to how many works there are
# - and

def createFic(*args):
    return{"hits": int(args[0]), "kudos": int(args[1]), "title": args[2], "author": args[3], "summary": args[4],
           "link": args[5], "quality": int(args[1])/int(args[0])}


class Fic:

    def __init__(self, *args):
        self.hits = int(args[0])
        self.kudos = int(args[1])
        self.title = args[2]
        self.author = args[3]
        self.summary = args[4]
        self.link = args[5]
        self.quality = self.prime_tasty()
        # needs to eat link obviously
        # language =
        # warnings =

    def prime_tasty(self):
        # make it depend on the number of pages
        # if self.kudos < 5:
        #    return 0

        return self.kudos / self.hits
    # nie liczy jak zero
    # jakies minimum kudosow
    # w pozniejszej zabawie mozna dodac bookmarki komentarze
    # language, warnings!!

    def fprint(self):
        print(self.title)
        print(self.author)
        print(self.link)
        print(self.hits)
        print(self.kudos)
        print(self.summary)
        print("\n")


class Search:

    Fics = []

    def __init__(self, *args):
        # function to ao3ify that string of a bitch
        self.tag = self.ao3ify_str(args[0])
        # check if tag ready or search it
        # make tag into soup
        self.soup = self.soupify()
        # find number of pages
        self.pages = int(self.find_pages())
        # approximate min number of kudos based on the num of works/pages
        if self.pages < 100:
            self.min_kudos = self.pages
        else:
            self.min_kudos = 100

    def search(self):
        user_input = [('work_search[query]', self.tag)]
        base_url = "https://archiveofourown.org/works/search?utf8="
        ao3search = requests.get(base_url, params=user_input)

    def soupify(self):

        base_url = "https://archiveofourown.org/tags/{tag}/works?page={number}"
        url = base_url.format(tag=self.tag, number=1)

        print(url)
        request = requests.get(url)
        src = request.content
        return BeautifulSoup(src, 'html.parser')
        # print(soup.prettify())

    def find_pages(self):
        pages = self.soup.find("ol", "pagination")
        lilist = pages.find_all("li")
        print(lilist[-2].get_text())
        if not lilist:
            return 1
        return lilist[-2].get_text()

    def eat_fics(self):
        base_url = "https://archiveofourown.org/tags/{tag}/works?page={number}"

        for i in range(1, self.pages):
            url = base_url.format(tag=self.tag, number=i)
            request = requests.get(url)
            src = request.content
            soup = BeautifulSoup(src, 'html.parser')
            works = soup.find_all("li", "work")
            print(i)
            for x in works:
                # make link from the numbers
                # maybe first get the important stuff for calculaitons, then details - title, author etc
                link = x.get('id')
                link = link.split("_")[1]
                ao3 = "https://archiveofourown.org/works/{}"
                link = ao3.format(link)

                hits = x.find("dd", "hits").get_text()
                if not x.find("blockquote", "summary"):
                    summary = " "
                else:
                    summary = x.find("blockquote", "summary").get_text()

                # THERE MIGHT BE A BETTER WAY TO DO THIS
                titleauthor = x.find("h4", "heading")
                talinks = titleauthor.find_all("a")
                title = talinks[0].get_text()
                if len(talinks) < 2:
                    author = "unknown"
                else:
                    author = talinks[1].get_text()

                if not (x.find("dd", "kudos")):
                    kudos = 0
                else:
                    kudos = x.find("dd", "kudos").get_text()
                # only create//append fic after checking worth

                if int(kudos) >= self.min_kudos:
                    ficcy = createFic(hits, kudos, title, author, summary, link)
                    #
                    if self.check_worth(ficcy):

                        if len(self.Fics) == 10:  # magic number - make it depend on how many pages there are
                            self.Fics.remove(self.minf())
                        self.Fics.append(ficcy)

    def print_best(self):
        print("printing best")
        # for x in self.Fics:
            # x.fprint()

    def minf(self):
        fmin = self.Fics[0]
        for i in self.Fics:
            if i["quality"] < fmin["quality"]:
                fmin = i
        return fmin

    def check_worth(self, fic):
        if len(self.Fics) < 10:
            return True
        if fic["quality"] > self.minf()["quality"]:
            return True
        else:
            return False

    def ao3ify_str(self, ao3str):
        changes = OrderedDict([(" ", "%20"), ("/", "*s*"), (".","*d*"), ("|", "%7C")]) # no need for ordered dicts, they are ordered now
        for i, j in changes.items():
            ao3str = ao3str.replace(i, j)

        return ao3str
