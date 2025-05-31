import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('2023_nba_player_stats.csv')
    df['Min_per_game'] = df['Min'] / df['GP']
    df['PTS_per_game'] = df['PTS'] / df['GP']
    df['AST_per_game'] = df['AST'] / df['GP']
    df['REB_per_game'] = df['REB'] / df['GP']
    df['AST_TOV'] = df['AST'] / df['TOV'].replace(0, pd.NA)
    return df

df = load_data()

st.title('NBA 2022-2023 Player Dashboard')

teams = ['All'] + sorted(df['Team'].unique())
positions = ['All'] + sorted(df['POS'].unique())
team = st.sidebar.selectbox('Team', teams)
pos  = st.sidebar.selectbox('Position', positions)

mask = True
if team != 'All':
    mask &= df['Team'] == team
if pos != 'All':
    mask &= df['POS'] == pos
data = df[mask]

col1, col2, col3 = st.columns(3)
col1.metric('PTS / G', f"{data['PTS_per_game'].mean():.1f}")
col2.metric('AST / G', f"{data['AST_per_game'].mean():.1f}")
col3.metric('REB / G', f"{data['REB_per_game'].mean():.1f}")

st.subheader('Plus-Minus vs Minutes')
fig1, ax1 = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=data, x='Min_per_game', y='+/-', hue='POS',
                s=50, alpha=0.7, edgecolor=None, ax=ax1)
ax1.set_xlabel('Minutes per Game'); ax1.set_ylabel('Plus-Minus')
st.pyplot(fig1)

st.subheader('Assist-to-Turnover Ratio')
fig2, ax2 = plt.subplots(figsize=(7, 5))
sns.boxplot(data=data, x='POS', y='AST_TOV', palette='pastel', ax=ax2)
ax2.set_xlabel('Position'); ax2.set_ylabel('AST / TOV'); ax2.set_ylim(0, 6)
st.pyplot(fig2)

st.subheader('Correlation Matrix')
metrics = ['Min_per_game', 'PTS_per_game', 'AST_per_game',
           'REB_per_game', 'Age', 'FG%']
corr = df[metrics].corr()
fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax3)
st.pyplot(fig3)
