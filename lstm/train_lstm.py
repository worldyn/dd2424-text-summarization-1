"""
Main entry to train LSTM summary model
"""
import os
import typing

import torchtext.vocab as vocab
import pytorch_lightning as pl

pl.seed_everything(1, workers=True)

from logger import logger
from model_v2 import LSTMSummary
from dataloader import create_dataloader
from config import config

from glove import extend_glove

glove = extend_glove(vocab.GloVe(name='6B', dim=50))


def main():
    data_dir = os.path.join(os.path.dirname(os.getcwd()), 'data', 'amazon-product-reviews')
    train_csv = os.path.join(data_dir, 'train_dev.csv')
    val_csv = os.path.join(data_dir, 'val_dev.csv')
    test_csv = os.path.join(data_dir, 'test_dev.csv')

    logger.info("Loading train data...")
    train_loader = create_dataloader(csv_file=train_csv, shuffle=True)

    logger.info("Loading val data...")
    val_loader = create_dataloader(csv_file=val_csv, shuffle=False)

    logger.info("Loading test data...")
    test_loader = create_dataloader(csv_file=test_csv, shuffle=False)

    vocab_size = len(glove.stoi.keys())
    model = LSTMSummary(input_size=vocab_size, hidden_size=config.HIDDEN_SIZE, output_size=vocab_size)
    print(model)
    
    trainer = pl.Trainer(
        gpus=1,
        fast_dev_run=False,
        max_epochs=config.EPOCHES,
        val_check_interval=config.VAL_CHECK_STEP,
        gradient_clip_val=1.0
    )
    trainer.fit(model, train_loader, val_loader)


if __name__ == '__main__':
    main()
