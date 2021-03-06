import numpy as np
import matplotlib.pyplot as plt
import sys

INPUT_FILE_NAME = 'yelp.csv'
f = open(INPUT_FILE_NAME, 'r', encoding="utf8")


data = []
############################ Part 1: Process data and formulate problem ###########################
isFirstLine = True
for line in f:
  if isFirstLine:
    # skip first line (headers)
    isFirstLine = False
    continue

  data_row = line.strip().split(',')[2:] # strip off id and name
  # find where "yelping since" is (dedault idx 1), so we can handle cases where name includes comma
  data_start_idx = 0
  for i in range(1, len(data_row)):
    if data_row[i].find('-') > 0:
      break
    else:
      data_start_idx += 1
  data_row  = data_row[data_start_idx:]
  data_row[1] = data_row[1].replace('-', '') # format date as number
  if len(data_row) >  19:
    # has more than one elite year, then count how many there are, and use that as a feature
    years = data_row[6:-12]
    data_row = data_row[:6] + [len(years)] + data_row[-12:]
  else:
    data_row[6] = 0 if data_row[6] == 'None' else 1

  # map to float so we can process as numpy array
  data_row = list(map(float, data_row))

  if data == []:
    data = [data_row]
  else:
    data.append(data_row)

data = np.asarray(data)
mins = np.amin(data, axis = 0)
maxs = np.amax(data, axis = 0)
data = (data - mins) / (maxs - mins)
print(data)

############################# problem 2 ###################################
#online K-means Algorithm (mini-batch)
import random

#get K random centroids(randomly select K data points, not using k-means++)
indices = random.sample(range(data.shape[0]), K)
centroids = data[indices]
def run_kmeans(data, K, centroids):
  B = 1000 #batch-size
  T = 300 #max number of iterations
  for t in range(1, T+1):
    eta = 1/t

    #randomly get mini-batch size data points
    mini_batch_indices = random.sample(range(data.shape[0]), B)
    batch_points = data[mini_batch_indices]

    #calculate the center(x)
    for i in range(B):
      x_i = batch_points[i]
      center_index = center(x_i, centroids)

      #update the cur_center
      centroids[center_index] += eta * (x_i - centroids[center_index])
  return centroids

####################### problem 3 ####################################
#return minimum distance square of the point and the current centroids
def min_distance(x, centroids):
    diff = centroids - x
    diff = diff**2
    return min(np.sum(diff, axis = 1))

  #return minimum distance square of the point and the current centroids
def get_distance(data, centroid):
    diff = data - centroid
    diff = diff**2
    return np.sum(diff, axis = 1)

#return np array
def kmpp_seeding(K, data):
    centroids = np.zeros([K, data.shape[1]])
    centroids[0] = data[random.sample(range(data.shape[0]), 1)]
    # distance_list = [0.0]*data.shape[0]

    min_distance = np.ones(data.shape[0])*float("inf")
    data_index = list(range(0,len(data)))
    for i in range(1, K):
        cur_distance = get_distance(data, centroids[i-1])
        min_distance = np.minimum(cur_distance, min_distance)
        Probability = min_distance/sum(min_distance)
        centroid_index = np.random.choice(data_index,1,list(Probability))[0]
        centroids[i] = data[centroid_index]
    return centroids


############################# problem 4 ####################################
def my_seeding(K, data):
    centroids = np.zeros([K, data.shape[1]])
    centroids[0] = data[random.sample(range(data.shape[0]), 1)]

    min_distance = np.ones(data.shape[0])*float("inf")
    data_index = list(range(0,len(data)))
    for i in range(1, K):
        cur_distance = get_distance(data, centroids[i-1])
        min_distance = np.minimum(cur_distance, min_distance)
        centroid_index = np.argmax(min_distance)
        centroids[i] = data[centroid_index]
    return centroids

################################## part 5 ##################################
def calculate_distances(data, centroids):
  distances = np.zeros((data.shape[0],))
  print(distances.shape)
  for i in range(data.shape[0]):
    distances[i] = np.amin(np.sum(np.sqrt((data[i] - centroids)**2), axis = 1))
  return distances

k_list = [5, 10, 50, 100, 200, 300, 400, 500]
random_distance_list = np.zeros((len(k_list), 3))
kmpp_distance_list = np.zeros((len(k_list), 3))
my_distance_list = np.zeros((len(k_list), 3))
for i, k in enumerate(k_list):
  # random init (p2)
  indices = random.sample(range(data.shape[0]), K)
  random_centroids = data[indices]
  random_centroids = run_kmeans(data, k, random_centroids)
  random_distances = calculate_distances(data, random_centroids)
  random_distance_list[i] = np.amin(random_distances), np.mean(random_distances), np.amax(random_distances)
  # kmpp init (p3)
  kmpp_centroids = kmpp_seeding(k, data)
  kmpp_centroids = run_kmeans(data, k, kmpp_centroids)
  kmpp_distances = calculate_distances(data, kmpp_centroids)
  kmpp_distance_list[i] = np.amin(kmpp_distances), np.mean(kmpp_distances), np.amax(kmpp_distances)
  # my init (p4)
  my_centroids = my_seeding(k, data)
  my_centroids = run_kmeans(data, k, my_centroids)
  my_distances = calculate_distances(data, my_centroids)
  my_distance_list[i] = np.amin(my_distances), np.mean(my_distances), np.amax(my_distances)

print(distance_list)
plt.plot(k_list, random_distance_list[:, 0], '-ro')
plt.plot(k_list, kmpp_distance_list[:, 0], '-go')
plt.plot(k_list, my_distance_list[:, 0], '-bo')
plt.title('Kmeans average min distance')
plt.xlabel('k')
plt.ylabel('Avg min distance')
plt.show()

plt.plot(k_list, random_distance_list[:, 1], '-ro')
plt.plot(k_list, kmpp_distance_list[:, 1], '-go')
plt.plot(k_list, my_distance_list[:, 1], '-bo')
plt.title('Kmeans average mean distance')
plt.xlabel('k')
plt.ylabel('Avg mean distance')
plt.show()

plt.plot(k_list, random_distance_list[:, 2], '-ro')
plt.plot(k_list, kmpp_distance_list[:, 2], '-go')
plt.plot(k_list, my_distance_list[:, 2], '-bo')
plt.title('Kmeans average max distance')
plt.xlabel('k')
plt.ylabel('Avg max distance')
plt.show()
