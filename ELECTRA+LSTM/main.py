import pandas as pd
import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup


import argparse
import gc

from utils import set_seed, EarlyStopping, log_metrics
from model import ELECTRALSTMClassification
from dataset import ELECTRALSTMDataset
from trainer import train, test


if __name__ == "__main__":

    device = "cuda" if torch.cuda.is_available() else "cpu"

    args = argparse.ArgumentParser()

    args.add_argument("--embedding_size", type=int, default=768)
    args.add_argument("--num_labels", type=int, default=44)
    args.add_argument("--dropout", type=float, default=0.1)
    args.add_argument("--batch_size", type=int, default=8)
    args.add_argument("--max_length", type=int, default=512)
    args.add_argument("--n_epochs", type=int, default=20)
    args.add_argument("--lr", type=float, default=1e-5)
    args.add_argument("--device", type=str, default=device)
    args.add_argument("--threshold", type=float, default=0.3)

    config = args.parse_args()
    
    set_seed(42)
    
    print("---prepare dataset---")
    train_dataset = ELECTRALSTMDataset("/train_data.pkl", config)
    valid_dataset = ELECTRALSTMDataset("/val_data.pkl", config)
    test_dataset = ELECTRALSTMDataset("/test_data.pkl", config)

    train_dataloader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
    valid_dataloader = DataLoader(valid_dataset, batch_size=config.batch_size, shuffle=False)
    test_dataloader = DataLoader(test_dataset, batch_size=config.batch_size, shuffle=False)
    print("---dataset is ready!---")
    
    model = ELECTRALSTMClassification(config).to(device)

    optimizer = AdamW(model.parameters(), lr=config.lr)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=2500, num_training_steps = 12500)

    early_stopping = EarlyStopping(patience=10, min_delta=0)
    best_val_loss = 1000

    print("---training start---")
    for epoch in range(config.n_epochs):
        gc.collect()
        torch.cuda.empty_cache()

        train_loss= train(model, train_dataloader, scheduler, optimizer, config)
        valid_loss, labels, preds = test(model, valid_dataloader, config)
        
        preds = torch.stack(preds)
        preds = torch.sigmoid(preds)
        preds = preds.cpu().detach().numpy()
        preds = np.where(preds > config.threshold, 1, 0)
        
        labels = torch.stack(labels)
        labels = labels.cpu().detach().numpy()
        
        auc_score = log_metrics(preds, labels)["auc_micro"]
        classification_report = log_metrics(preds, labels, config)["classification_report"]
        
        avg_train_loss, avg_val_loss = train_loss / len(train_dataloader), valid_loss / len(test_dataloader)

        print(f"[{epoch+1}/{config.n_epochs}]")
        print(f"AUC score: {auc_score}")
        print(f"Average Train Loss: {avg_train_loss}")
        print(f"Average Valid Loss: {avg_val_loss}")
        print(classification_report)
        print("\n")

        early_stopping(avg_val_loss)
        if early_stopping.early_stop:
            break

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), "./best_model.pt")
            print(f"Model saved as current valid loss: {best_val_loss}")
            
    test_loss, labels, preds = test(model, test_dataloader, config)
    avg_test_loss = test_loss / len(test_dataloader)
    
    auc_score = log_metrics(preds, labels)["auc_micro"]
    classification_report = log_metrics(preds, labels, config)["classification_report"]
    
    print("<test result>")
    print(f"AUC score: {auc_score}")
    print(f"Test Loss: {avg_test_loss}")
    print(classification_report)