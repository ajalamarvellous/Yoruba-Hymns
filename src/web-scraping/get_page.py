import requests

def get_page(url: str):
    """Gets the url page requested for"""

    page = ""
    try:
        page = requests.get(url, verify=False)
    except Exception as err:
        print(f"An error occured: {err}")
    return page

if __name__ == "__main__":
    page = get_page(url)
    print(page.content)