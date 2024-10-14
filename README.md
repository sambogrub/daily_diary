# Daily Diary
 Initial thoughts were to make an app that would act as a daily journal along with
 a daily goal tracker and visualization. 
 
I have gone through multiple iterations of this idea, and have settled on building
it using layerd architecture. 

## Installation
You'll need a working Python3 on your machine, preferably Python 3.10
or [newer](https://www.python.org/downloads/). 

1. Clone the project from GitHub [repository](https://github.com/sambogrub/daily_diary)
   ```shell
   git clone https://github.com/sambogrub/daily_diary.git
   ```
2. Create a dedicated virtual environment
   ```shell
   cd daily_diary
   python3 -m venv venv
   ```
3. Activate virtual environment
   * On Linux and macOS
     ```shell
     . venv/bin/activate
     ```
   * On Windows with PowerShell
     ```shell
     .\venv\Scripts\Activate.ps1
     ```
   * On Windows with CMD
     ```shell
     venv\scripts\activate.bat
     ```
4. Install dependencies
   ```shell
   python3 -m pip install -r requirements.txt
   ```

## To Run

1. Open the command line and go to the `daily_diary` folder
2. Activate the virtual environment (see [Installation instructions](#installation))
3. Start the app by typing
    ```
    python3 journal\main.py
    ```

### ⚠️Warning!
At the moment it does not run with a UI. It only has the business end of data access and month/day models.
