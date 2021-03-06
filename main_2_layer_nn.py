import numpy as np
from util import cifar_10, layer
import time

n_pixel = 3072
n_mid = 100
n_class = 10
step_size = 1e-4

layer_1 = layer.FCLayer(n_pixel, n_mid, step_size, "Softmax")
layer_2 = layer.FCLayer(n_mid, n_class, step_size, "Softmax loss")

batch = [None] * 5
batch[0] = cifar_10.unpickle("data_batch_1")
batch[1] = cifar_10.unpickle("data_batch_2")
batch[2] = cifar_10.unpickle("data_batch_3")
batch[3] = cifar_10.unpickle("data_batch_4")
batch[4] = cifar_10.unpickle("data_batch_5")
n_train = 10000

start = time.time()
for usage in range(1):
    for j in range(1):
        data = batch[j][b'data'] / 256
        label = batch[j][b'labels']
        for k in range(n_train):
            res_from_l1 = layer_1.train(data[k])
            res_from_l2 = layer_2.train(res_from_l1)
            grad_from_l2 = layer_2.backprop(label=label[k])
            grad_from_l1 = layer_1.backprop(upstream_grad=grad_from_l2)
print("--- Training time: {0:.4f}s".format((time.time() - start)))

batch_test = cifar_10.unpickle("test_batch")
data_test = batch_test[b'data'] / 256
label_test = batch_test[b'labels']
n_bingo = 0
n_test = 10000

start = time.time()
for k in range(n_test):
    res_from_l1 = layer_1.predict(data_test[k])
    res_from_l2 = layer_2.predict(res_from_l1)
    if np.argmax(res_from_l2) == label_test[k]:
        n_bingo += 1
print("--- Testing time: {0:.4f}s".format((time.time() - start)))
print("--- Accuracy on test data: {}%".format(n_bingo * 100 / n_test))
