dwlist = ["very", "really", "do", "reader", "said", "says", "shows", "lot", "thing", "anything",
          "something", "you", "we", "believe", "nice", "good", "done", "hard", "easy", "all"]


def word_search():
    file = open("searchforwords.txt", "r")
    data = file.read()
    data = data.split()
    for word in data:
        if word in dwlist:
            print(word + " was found in the text. Consider replacing it!")


word_search()
