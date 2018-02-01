# Only use what is provided in the standard libraries.
import os
import sys
import math
import string

''' This function reads in a file and returns a
	set of all the tokens. It ignores the subject line

	If the email had the following content:

	Subject: Get rid of your student loans
	Hi there,
	If you work for us, we will give you money
	to repay your student loans. You will be
	debt free!
	FakePerson_22393

	This function would return to you
	set(['', 'work', 'give', 'money', 'rid', 'your', 'there,',
		'for', 'Get', 'to', 'Hi', 'you', 'be', 'we', 'student',
		'debt', 'loans', 'loans.', 'of', 'us,', 'will', 'repay',
		'FakePerson_22393', 'free!', 'You', 'If'])
'''


# word_count: dictionary
def count(word_count, training_folder, training_set_is_ham):
    mails = os.listdir(training_folder)
    mail_count = len(mails)
    for filename in mails:
        tokens = token_set(training_folder + "/" + filename)
        translator = str.maketrans('', '', string.punctuation)
        for words in tokens:
            words = words.translate(translator)
            if not words in word_count:
                word_count[words] = [1, 1]
            word_count[words][training_set_is_ham] += 1
    return mail_count


def calculate(word_count, spam_count, ham_count):
    for words in word_count:
        counts_list = word_count[words]
        word_count[words][0] = counts_list[0] / (spam_count + 2)
        word_count[words][1] = counts_list[1] / (ham_count + 2)
    return word_count


def token_set(filename):
    # open the file handle
    with open(filename, 'r') as f:
        text = f.read()[9:]  # Ignoring 'Subject:'
        text = text.replace('\r', '')
        text = text.replace('\n', ' ')
        tokens = text.split(' ')
        return set(tokens)


def fileToInt(s):
    return int(s[:-4])


def main():
    # this is a dictionary, key would be unique words, value would be a list of [spam count, ham count]
    word_count = {}

    # count spam emails into the dictionary
    spam_training_folder = f"{sys.argv[1]}/train/spam"
    spam_count = count(word_count, spam_training_folder, 0)

    # count ham emails into the dictionary
    ham_training_folder = f"{sys.argv[1]}/train/ham"
    ham_count = count(word_count, ham_training_folder, 1)

    word_prob = calculate(word_count, spam_count, ham_count)
    spam_prob = spam_count / (spam_count + ham_count)
    ham_prob = ham_count / (spam_count + ham_count)

    test_folder = f"{sys.argv[1]}\\test"
    test_mails = sorted(os.listdir(test_folder), key=fileToInt)
    for filename in test_mails:
        tokens = token_set(test_folder + "/" + filename)
        file_spam_prob = math.log(spam_prob)
        file_ham_prob = math.log(ham_prob)
        translator = str.maketrans('', '', string.punctuation)
        for words in tokens:
            words = words.translate(translator)
            if words in word_prob:
                file_spam_prob = file_spam_prob + math.log(word_prob[words][0])
                file_ham_prob = file_ham_prob + math.log(word_prob[words][1])
        if file_spam_prob > file_ham_prob:
            print(f"{filename} spam")
        else:
            print(f"{filename} ham")


if __name__ == '__main__':
    main()
