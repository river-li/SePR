import seaborn as sns
import matplotlib.pyplot as plt
import torch
import torchviz
from sklearn.manifold import TSNE

def draw_boxplot(feature, label):
    colname = ['files changed', 'lines added', 'lines removed', 'loops added',
               'loops removed', 'ifs added', 'ifs removed', 'boolean_op added',
               'boolean_op removed', 'pairs added', 'pairs removed',
               'function calls added', 'function calls removed',
               'assignment added', 'assignment removed', 'sizeof added',
               'sizeof removed', 'continue added', 'continue removed',
               'break added', 'break removed', 'goto added', 'goto removed',
               'return added', 'return removed', 'numerical added',
               'numerical removed', 'compare added', 'compare removed',
               'error added', 'error removed']
    plt.figure()
    for featureid in range(len(colname)):
        plt.subplot(4, 8, featureid + 1)
        sns.boxplot(x=label, y=feature[:, featureid])
        plt.title(colname[featureid])
    plt.subplots_adjust(hspace=0.4)
    plt.show()


def drawNN(nn,output_path):
    x = torch.rand(size=(1, 32), requires_grad=True)
    NN_image = torchviz.make_dot(nn(x), params=dict(list(nn.named_parameters()) + [('x', x)]))
    NN_image.format = 'svg'
    NN_image.directory = output_path
    NN_image.view()
