from chainer import Chain
import chainer.functions as F
import chainer.links as L


class MyModel(Chain):

    def __init__(self, n_out=12):
        super(MyModel, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, 128)
            self.l2 = L.Linear(None, 64)
            self.l3 = L.Linear(None, n_out)

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)





