import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Evidence is a list of lists
    evidence = []

    # Label is a list of values
    labels = []

    # Indices we want to convert to integers
    int_set = {0, 2, 4, 11, 12, 13, 14}

    # Indices we want to convert to floats
    float_set = {1, 3, 5, 6, 7, 8, 9}

    # Other special indices
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    visitor = ["New_Visitor", "Returning_Visitor"]
    tf = ["FALSE", "TRUE"]

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        # Skip header:
        next(reader, None)
        # Iterate through each row in csv file
        for row in reader:

            row_list = []

            # Iterate through each item in row
            for i in range(0, len(row)):

                if i in int_set:
                    row_list.append(int(row[i]))
                
                elif i in float_set:
                    row_list.append(float(row[i]))

                elif i == 10: 
                    month_i = months.index(row[i])
                    row_list.append(month_i)
                
                elif i == 15:
                    try:
                        row_list.append(visitor.index(row[i]))
                    # Catch "Other"
                    except: 
                        row_list.append(0)
                    
                elif i == 16:
                    row_list.append(tf.index(row[i]))

                # Label
                elif i == 17:
                    labels.append(tf.index(row[i]))
    
            evidence.append(row_list)

    return((evidence, labels))


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    sensitivity_correct = 0
    sensitivity_total = 0

    specificity_correct = 0
    specificity_total = 0

    # Check correctness
    for i in range(0, len(labels)):
        # No Buy
        if labels[i] == 0:
            specificity_total += 1
            if labels[i] == predictions[i]:
                specificity_correct += 1
        else:
            sensitivity_total += 1
            if labels[i] == predictions[i]:
                sensitivity_correct += 1

    
    return ((sensitivity_correct/sensitivity_total), (specificity_correct/specificity_total))


if __name__ == "__main__":
    main()
