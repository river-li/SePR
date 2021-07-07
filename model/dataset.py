import torch
from torch.utils.data import TensorDataset
import numpy as np
from scripts.parse_spi_samples import parse_csv


def generate_qemu_dataset():
    qemu_sep, qemu_nsep = parse_csv('./data/spi/qemu.csv', False)
    qemu_sep = np.array(qemu_sep)
    qemu_nsep = np.array(qemu_nsep)

    qemu_data = np.vstack((qemu_sep, qemu_nsep))
    qemu_label = np.hstack((np.ones(len(qemu_sep)), np.zeros(len(qemu_nsep))))
    # 4932 positive, 6977 negative
    # 11909 in total

    np.random.seed(1234)
    np.random.shuffle(qemu_data)
    np.random.seed(1234)
    np.random.shuffle(qemu_label)
    qemu_data = torch.Tensor(qemu_data)
    qemu_label = torch.Tensor(qemu_label).long()

    train_data = TensorDataset(qemu_data[:8000], qemu_label[:8000])
    validation_data = (qemu_data[8000:9600], qemu_label[8000:9600])
    test_data = (qemu_data[9600:], qemu_label[9600:])

    return train_data, validation_data, test_data


def generate_ffmpeg_dataset():
    ffmpeg_sep, ffmpeg_nsep = parse_csv('./data/spi/ffmpeg.csv', False)
    ffmpeg_sep = np.array(ffmpeg_sep)
    ffmpeg_nsep = np.array(ffmpeg_nsep)

    ffmpeg_data = np.vstack((ffmpeg_sep, ffmpeg_nsep))
    ffmpeg_label = np.hstack((np.ones(len(ffmpeg_sep)), np.zeros(len(ffmpeg_nsep))))
    # 5962 positive, 8000 negtive
    # 13962 in total

    np.random.seed(5678)
    np.random.shuffle(ffmpeg_data)
    np.random.seed(5678)
    np.random.shuffle(ffmpeg_label)

    ffmpeg_data = torch.Tensor(ffmpeg_data)
    ffmpeg_label = torch.Tensor(ffmpeg_label).long()

    train_data = TensorDataset(ffmpeg_data[:9600], ffmpeg_label[:9600])
    validation_data = (ffmpeg_data[9600:10240], ffmpeg_label[9600:10240])
    test_data = (ffmpeg_data[10240:], ffmpeg_label[10240:])

    return train_data, validation_data, test_data


qemu_train_data, qemu_validation_data, qemu_test_data = generate_qemu_dataset()
ffmpeg_train_data, ffmpeg_validation_data, ffmpeg_test_data = generate_ffmpeg_dataset()
