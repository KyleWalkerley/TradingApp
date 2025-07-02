import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def prepare_ml_data(df):
    df = df.copy()
    
    # Create target: 1 if next day price is higher, else 0
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    
    # Features for the model
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Drop rows with NaNs *after* all indicators are calculated
    df = df.dropna()
    
    # Final features and labels
    X = df[['Close', 'SMA50', 'SMA200', 'RSI']]
    y = df['Target']
    return X, y

def train_predict_model(df):
    X, y = prepare_ml_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))

    # Predict for the most recent day
    latest = X.iloc[[-1]]
    prediction = model.predict(latest)[0]
    probability = model.predict_proba(latest)[0][prediction]
    
    return prediction, probability, accuracy
