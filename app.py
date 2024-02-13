import streamlit as st
import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

symbol_count = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}

symbol_value = {
    'A': 10,
    'B': 6,
    'C': 4,
    'D': 2
}

def getSpin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        all_symbols.extend([symbol] * symbol_count)

    columns = []
    for _ in range(cols):
        column = random.sample(all_symbols, rows)
        columns.append(column)
    
    return columns

def checkWinnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    # Check horizontal lines
    for row in range(lines):
        symbol = columns[row][0]
        if all(symbol == columns[row][col] for col in range(len(columns[row]))):
            winnings += values[symbol] * bet
            winning_lines.append(row + 1)

    return winnings, winning_lines


def main():
    st.title("Slot Machine Game 🎰")

    if 'balance' not in st.session_state:
        st.session_state.balance = 0

    balance = st.sidebar.number_input('Deposit amount:', min_value=0, value=st.session_state.balance)

    if st.sidebar.button('View Balance'):
        st.sidebar.text(f'Your current balance is ${balance}')

    lines = st.sidebar.slider('Number of lines (1-3):', 1, MAX_LINES, 1)
    bet = st.sidebar.slider('Bet amount ($1-$100):', MIN_BET, MAX_BET, 1)
    total_bet = bet * lines
    st.text(f'You are betting ${bet} on {lines} lines.')
    st.text(f'Total Bet: ${total_bet}')
    st.text('Best of Luck🤞')

    if st.sidebar.button('Spin'):
        if total_bet > balance:
            st.error('You do not have enough balance to bet!! 😔')
        else:
            balance -= total_bet
            slots = getSpin(ROWS, COLS, symbol_count)
            result = '\n'.join([' | '.join(column) for column in slots])
            st.text(result)

            winnings, winning_lines = checkWinnings(slots, lines, bet, symbol_value)
            if winnings > 0:
                balance += winnings
                st.text(f'You won ${winnings} 💰')
                st.text('You won on lines: ' + ', '.join(map(str, winning_lines)))
            else:
                st.text('You did not win anything.')

    if st.sidebar.button('Respin'):
        total_bet = bet * lines
        st.text(f'You are betting ${bet} on {lines} lines.')
        st.text(f'Total Bet: ${total_bet}')
        if total_bet > balance:
            st.error('You do not have enough balance to bet!!')
            st.error(f'Remaining Balance: ${balance}')
        else:
            balance -= total_bet
            slots = getSpin(ROWS, COLS, symbol_count)
            result = '\n'.join([' | '.join(column) for column in slots])
            st.text(result)

            winnings, winning_lines = checkWinnings(slots, lines, bet, symbol_value)
            if winnings > 0:
                balance += winnings
                st.text(f'You won ${winnings} 💸')
                st.text('You won on lines: ' + ', '.join(map(str, winning_lines)))
            else:
                st.text('You did not win anything 🥲')

    if st.sidebar.button('Quit'):
        st.stop()

    st.session_state.balance = balance

if __name__ == "__main__":
    main()
