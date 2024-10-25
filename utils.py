import pandas as pd
import torch
import numpy as np

def pandas_player_match(player_matches):

    match_data = pd.DataFrame(player_matches, columns=[
        'Date', 
        'Tournament Name', 
        'Surface', 
        'Tournament level', 
        'Status',
        'Rank', 
        'Seed', 
        'Round', 
        'Score', 
        'Opp Name', 
        'Opp Rank', 
        'Opp Seed', 
        'Opp Hand', 
        'Opp BDay', 
        'Opp Height', 
        'Opp Nationality'
    ])

    match_data['Date'] = pd.to_datetime(match_data['Date'])
    match_data.set_index('Date', inplace=True)
    match_data.sort_index(inplace=True, ascending=False)


    return match_data



def train_step(model: torch.nn.Module,
               dataloader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
               optimizer: torch.optim.Optimizer,):
    
    model.train()

    train_loss, train_acc = 0, 0

    for batch, (X, y) in enumerate(dataloader):
        y_pred = model(X)
        loss = loss_fn(y_pred, y)
        train_loss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epsilon = 1e-8
        train_acc += (np.abs(y_pred.detach() - y.detach())/(y.detach() + epsilon)).sum().item() / len(y_pred)
    
    train_loss = train_loss / len(dataloader)
    train_acc = train_acc / len(dataloader)
    return train_loss, train_acc


def test_step(model: torch.nn.Module,
              dataloader: torch.utils.data.DataLoader,
              loss_fn: torch.nn.Module,):
    
    model.eval()

    test_loss, test_acc = 0, 0

    with torch.inference_mode():
        for batch, (X, y) in enumerate(dataloader):
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            test_loss += loss.item()
            epsilon = 1e-8
            test_acc += (np.abs(y_pred.detach() - y.detach())/(y.detach() + epsilon)).sum().item() / len(y_pred)
        
        test_loss += test_loss / len(dataloader)
        test_acc += test_acc / len(dataloader)
        return test_loss, test_acc 


def train(model: torch.nn.Module,
          train_dataloader: torch.utils.data.DataLoader,
          test_dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module,
          epochs: int = 5,):
    
    results = {"train_loss": [],
                "train_acc": [],
                "test_loss": [],
                "test_acc": []}
    
    for epoch in range(epochs):
        train_loss, train_acc = train_step(model=model,
                                           dataloader=train_dataloader,
                                           loss_fn=loss_fn,
                                           optimizer=optimizer,)
        test_loss, test_acc = test_step(model=model,
                                        dataloader=test_dataloader,
                                        loss_fn=loss_fn,)

        print(f"Epoch: {epoch} | Train loss: {train_loss:.4f} | Train acc: {train_acc:.4f} | Test loss: {test_loss:4f} | Test acc: {test_acc:.4f}")
        results["train_loss"].append(train_loss)
        results["train_acc"].append(train_acc)
        results["test_loss"].append(test_loss)
        results["test_acc"].append(test_acc)       

    return results               


