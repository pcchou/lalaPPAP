lalaPPAP - Prickly Pear for All Posts (for 拉拉(?))
================================================

![Prickly Pear](http://i.imgur.com/8w8bSlK.jpg)
* Shown above is an example of Prickly Pear sticker. (Copyright belongs to Facebook Inc.)

## Usage

1. 用 `git clone https://github.com/pcchou/lalaPPAP` 下載這個專案。（你也可以使用 zip 檔）<br>
   Clone this project with the git command above.
2. 用 `pip install -r requirements.txt` 安裝需求套件。<br>
   Install third-party dependencies with the command above.
3. 把 `data.example.py` 改成 `data.py`，並且填入你的 cookie 資訊及相關設定<br>
   Rename `data.example.py` to `data.py` and fill in your cookie credentials and related information.
5. 將 `check.py` 加到 `crontab`，或是你的作業系統排程器中<br>
   Add `check.py` to your `crontab` (or your own OS time scheduler).
  * 例如：`* * * * * /usr/bin/python3 $HOME/git/lalaPPAP/check.py`


## Demo

![img](https://cloud.githubusercontent.com/assets/5615415/21482733/dcbcbcca-cbb2-11e6-9275-23b73d9a7f05.png)
