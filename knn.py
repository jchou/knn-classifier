import numpy
import operator

def k_nearest(x, observations, k):
    x = map(float, x.split(','))
    x = numpy.array(x)
    y = numpy.array(observations)
    distances = numpy.sqrt(numpy.sum(numpy.square(x - y), axis=1))
    k_nearest_dists = numpy.sort(distances)[:k]
    k_nearest_indices = distances.argsort()[:k]

    return zip(k_nearest_dists, k_nearest_indices)


def classify_all(features_file, out_labels_file, k):
    with open("trainFeatures.csv") as training_features,\
            open("trainLabels.csv") as training_labels,\
            open(features_file) as all_features,\
            open(out_labels_file, 'w') as labels:
        training_features = training_features.read().splitlines()
        training_features = [map(float, observation.split(',')) for observation in training_features]
        training_labels = training_labels.read().splitlines()
        all_features = all_features.read().splitlines()

        results = []
        for features in all_features:
            classes = [0] * 10
            for distance, index in k_nearest(features, training_features, k):
                classes[int(training_labels[index])] += 1
            cls = max(enumerate(classes), key=operator.itemgetter(1))[0]
            results.append(str(cls))
        labels.write('\n'.join(results))


def error_rate(file1, file2):
    with open(file1) as data1, open(file2) as data2:
        both = zip(data1, data2)
        errors = [error for error in enumerate(both) if int(error[1][0].strip()) != int(error[1][1].strip())]
        for error in errors:
            print error
        print str(len(errors)) + " errors"
