# etherscan-label-fetcher

This project is a tool for fetching the addresses & tokens available in any etherscan-like blockchain explorer.

## Dependencies
This project was developed using `python3.7.4` and all the libraries used are bultin.

## Usage

To fetch the addresses you will need a valid `sessionId` for the explorer from where you want to fetch the data. You
can find this value (assuming you are using Chrome) by doing the following:
- open the explorer
- go to `<explorer-url>/labelcloud`
- sign in
- open the browser inspector (ctrl+shift+C)
- go to `Network` tab
- press `Doc` filter
- select `labelcloud`
- go to Headers -> Request Headers -> cookie
- copy the value of `ASP.NET_SessionId` property

After that you will be able to run:
```python
python main.py -s your-sessionId
```
By default that will show you all the accounts with `phish-hack` label in etherscan.

The program has support for chanching some values in command line:
- `--label/-l` allows you to change the label fetched (default `phish-hack`)
- `--token/-t` allows you to fetch the tokens instead of the accounts 
- `--explore/-e` allows you to change the explorer url (default `https://etherscan.io`)
- `--offset/-o` allows you to change the number of addresses to skip (default `0`)

So you can fetch the tokens marked as `entertainment` on bscscan with the following command:
```python
python main.py -s your-bscscan-sessionID -e https://bscscan.com/ -t -l entertainment
```

