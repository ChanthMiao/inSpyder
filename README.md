# inSpyder

The inSpyer toolset provides an easy way to automatically pull users' data, including profile and posts, from instagram with theme list. All the data are stored in local database.

## Function

|      script      | functon                    |
| :--------------: | -------------------------- |
|    orm/sql.py    | Database operation manager |
|   inSpyder.py    | Data capture               |
| pic_downloads.py | Picture downloading        |
|    visual.py     | Data visualization         |

## Python dependences

**For data capture and storage**

- requests
- sqlalchemy (libs like psycopg2 may required, depending on your database.)

**For data visualization**

- numpy
- matplotlib
- jieba
- wordcloud

## Database

All direct operations that related with database is done by sqlalchemy. For convenience, I hard code my local database connection info  `"postgresql://inspyder:No996icu@127.0.0.1:5432/insdata"` in the project. You need to modify it into your's to run it.

## Proxy

For some reason, you may be unable to directly get access to instagram, which means that a proxy is needed. I failed to set proxy directly with requests lib. Instead, I simply set two env variables below before run the script.

```bash
export http_proxy="http://your_proxy_host:port"
export https_proxy="http://your_proxy_host:port"
```
## Run

Offer a theme list in ./themes.json like below. Use '+' instead of ' '.

```json
{
    "themes": [
        "network+security",
        "cybersecurity",
        "information+security"
    ]
}
```

Then simply call the python interrupter.

```bash
python inSpyder.py
python pic_downloads.py
python visual.py
```
