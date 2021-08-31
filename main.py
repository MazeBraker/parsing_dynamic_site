import requests
import json
import os
import time

# lets look for data that sends the site
# inspect -> network(make 1 request)->www...->User-agent : , accept : 

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def get_data_file(headers):
    """Collest data and return a JSON file"""
    # req url
    # we made request and index.html to see div block with cards info is empty 3445 line,
    # we could have used selenium methods, but not this time
    # URL = "https://www.landingfolio.com/"
    # r = requests.get(url=URL, headers=headers)
    # # save page
    # with open("index.html", "w") as file:
    #     file.write(r.text)
    offset = 0
    result_list = []
    img_count = 0
    while True:
        url = f"https://s1.landingfolio.com/api/v1/inspiration/?offset={offset}&color=%23undefined"

        response = requests.get(url=url, headers=headers)
        data = response.json()
        for item in data:
            # without domain download link is useless(for images "url": "1630392265362-tailory-logo.png"),
            # so inspect image itself and get link
            # https://landingfoliocom.imgix.net/1630392265382-tailory-landing-page-desktop
            # .png?lossless=true&fit=crop&w=360&h=600&crop=top,left&auto=format&q=75
            if "description" in item:
                "https://landingfoliocom.imgix.net/"
                images = item.get("images")
                img_count += len(images)  # длина списка со словарями в которых хранятся images

                for img in images:
                    img.update({"url": f"https://landingfoliocom.imgix.net/{img.get('url')}"})
                result_list.append({
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "url": item.get("url"),
                    "images": images
                })
            else:  # got everything
                with open("result_list.json", "a") as file:
                    json.dump(result_list, file, indent=4, ensure_ascii=False)
                return f"[INFO] WORK IS DONE. Images count is: {img_count}\n{'=' * 20}"
        print(f"[+] Processed {offset}")
        offset += 1


# download images and sort them by directories


def download_imgs(file_path):
    """Download images"""
    # pass
    # check path
    try:
        with open(file_path) as file:
            src = json.load(file)

    except Exception as _ex:
        print(_ex)
        return "[INFO] Chech the file path!"

    items_len = len(src)
    count = 1

    for item in src[:10]:
        item_name = item.get("title")
        item_imgs = item.get("images")

        if not os.path.exists(f"data/{item_name}"):
            os.mkdir(f"data/{item_name}")

        for img in item_imgs:
            r = requests.get(url=img["url"])

            with open(f"data/{item_name}/{img['type']}.png", "wb") as file:
                file.write(r.content)
        print(f"[+] Download {count}/{items_len}")
        count += 1
    return "[INFO] WORK FINISHED"


# here we call our functions
def main():
    start_time = time.time()
    # print(get_data_file(headers=headers))
    print(download_imgs("result_list.json"))

    finished_time = time.time() - start_time
    print(f"Worked time: {finished_time}")


if __name__ == "__main__":
    main()
