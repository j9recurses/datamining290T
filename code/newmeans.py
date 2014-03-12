###
# Implement simple k-means clustering using 1 dimensional data
#
##/
import random

dataset = [
    -13.65089255716321, -0.5409562932238607, -88.4726466247223,
    39.30158828358612, 4.066458182574449, 64.64143300482378,
    38.68269424751338, 33.42013676314311, 31.18603331719732,
    -0.2027616409406292, 45.13590038987272, 30.791899783552395,
    61.1727490302448, 18.167220741624856, 88.88077709786394,
    -1.3808002119514704, 50.14991362212521, 55.92029956281276,
    -6.759813255299466, 34.28290084421072
]

k = 2  # number of clusters


###
# Helper functions
# Fill in TODOs where needed
##/

def pick_centroids(xs, k):
    """Return list of num centroids given a list of numbers in xs"""
    mymin = int(min(xs))
    print mymin
    mymax =  int(max(xs))
    print mymax
    centroids = []
    myk =  range(k)
   # while len(centroids) != len(set(centroids)) | len( centroids) == 0: 
    while len( centroids) == 0:
        while len(centroids) != len(set(centroids): 
            for k in myk:
                print "in the loop"
            
                 #print i
                centroids.append(random.randrange(mymin, mymax))
                print centroids
    print centroids
    return centroids


def distance(a, b):
    """Return the distance of numbers a and b"""
    distance = abs(a-b)
    return distance
    ##/


def centroid(xs):
    """Return the centroid number given a list of numbers, xs"""
    avg = (float(sum(xs))/float(len(xs)))
    print avg
    return avg

def cluster(xs, centroids):
    """Return a list of clusters centered around the given centroids.  Clusters
    are lists of numbers."""

    #clusters = [[] for c in centroids]
    #for x in xs:
        # find the closest cluster to x
    #   dist, cluster_id = min((distance(x, c), cluster_id) for cluster_id, c in enumerate(centroids))
        # place x in cluster
     #   clusters[cluster_id].append(x)
    #return clusters


def iterate_centroids(xs, centroids):
    """Return stable centroids given a dataset and initial centroids"""

    err = 0.001  # minimum amount of allowed centroid movement
    observed_error = 1  # Initialize: maxiumum amount of centroid movement
    new_clusters = [[] for c in centroids]  # Initialize: clusters

    while observed_error > err:
        new_clusters = cluster(xs, centroids)
        new_centroids = map(centroid, new_clusters)

        observed_error = max(abs(new - old) for new, old in zip(new_centroids, centroids))
        centroids = new_centroids

    return (centroids, new_clusters)


#### Main part of program: 
    # Pick initial centroid, iterative to find final centroids, Print results ##a
#####

initial_centroids = pick_centroids(dataset, k)
print initial_centroids
#final_centroids, final_clusters = iterate_centroids(dataset, initial_centroids)
##   print "Centroid: %s" % centroid
  #  print "Cluster contents: %r" % cluster
