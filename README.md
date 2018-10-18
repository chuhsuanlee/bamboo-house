# Welcome to bamboo-house

This project uses API provided by [Alpha Vantage](https://www.alphavantage.co/) as a tool to have a quick look on the Bitcoin stock market and derive some insights from it.

To run this project, an API key must be claimed beforehand. Please go to [this page](https://www.alphavantage.co/support/#api-key) and claim yours.

After cloning this repository to your local machine, substitute the **API_KEY** in [config.py](src/config.py) with the key retrieved from above.

There are some commands you can use as indicated in [Makefile](Makefile), or simply type `make help`, it will show the Make commands that can be used.

The main tasks in this project are:
* Download the historical daily data as a csv file and store it in [Downloads folder](src/Downloads/).
* Compute the average price of each week and store it on a csv file in [Reports folder](src/Reports/).
* Compute what is the week that had the greatest relative span on closing prices and print this on screen.

Example output after executing `make run`:
```bash
Successfully read 1661 daily data.
The greatest relative span happened in the week between 2015-01-12 and 2015-01-18 with the span of 0.50634769.
```
