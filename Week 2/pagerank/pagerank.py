import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize Dict with all pages in corpus
    Prob_distribution = {}
    for key in corpus:
        Prob_distribution[key] = 0

    # If there are links in the from our current page
    if len(corpus[page]) > 0:

        # Get the probability for each linked page
        probability = damping_factor/len(corpus[page])

        # Iterate through values the key has & assign probabilities in our distribution
        for value in corpus[page]:
            Prob_distribution[value] = probability

        # Get the probability for any random page
        probability2 = (1 - damping_factor)/len(corpus)

        # Iterate through all keys and add prob2
        for key in corpus:
            Prob_distribution[key] = Prob_distribution[key] + probability2

    # If there are no linked pages
    else:
        
        # Get an equal probability for every webpage
        probability3 = 1 / len(corpus)

        for key in corpus:
            Prob_distribution[key] = probability3


    return Prob_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a dictionary with all webpages to track counts
    counts = {}
    for key in corpus:
        counts[key] = 0

    # Choose first random sample & add count
    sample = random.choice(list(counts.keys()))
    counts[sample] += 1

    # Run through all samples
    for i in range(0, n):

        # Run transition model
        distribution = transition_model(corpus, sample, damping_factor)

        # Generate a new sample from probability distribution
        population = []
        weights = []
        for key, value in distribution.items(): 
            population.append(key)
            weights.append(value)
        
        # Since choices returns a list choose the item w/ index 0 (there is only one; you can specify multiple though with k)
        sample = random.choices(population=population, weights=weights)[0]

        # Increase count
        counts[sample] += 1

    # Transform into dictionary with probabilities
    for key in counts:
        counts[key] = counts[key] / n

    return counts


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    counts = {}
    total_pages = len(corpus)
    for key in corpus:
        # Assign initial equal PR to each page
        counts[key] = 1 / total_pages

        # Check if that key has no links
        if len(corpus[key]) == 0: 
            all_pages = set()
            for key_other in corpus: 
                all_pages.add(key_other)

            # Set the value of that key equal to a set with all pages
            corpus[key] = all_pages

    change = 1

    # While loop until change is less then 0.001
    while change > 0.001:
        
        for key in counts.keys():
            
            sum = 0

            # Check for pages linking to that page
            for other_key in corpus: 

                # Check whether the key is contained in the values set of other key
                if key in corpus[other_key]:
                    
                    # Divide the PR of the other key by the amount of links it contains
                    sum += counts[other_key] / len(corpus[other_key])

            # Derive new PR for key
            new_rank = (1 - damping_factor)/total_pages + damping_factor * sum

            # Check if change is less than 0.001
            change = abs(new_rank - counts[key])

            # Update PR
            counts[key] = new_rank

    return counts

if __name__ == "__main__":
    main()
