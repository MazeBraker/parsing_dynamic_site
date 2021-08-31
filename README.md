# Parsing dynamic site via python *(we want to make json file with all data, images from site)*

---

## Step by step instractions
1. Get headers with making request and analyze inspect page
2. See through index.html and find class related to cards images
3. `<div class="relative flex flex-wrap items-stretch w-full">`
main body is empty. We could have used selenium and parse site online, but not this time.
4. Go to main page and scroll it to see some responses in Network
5. Find api related and notice it's response. That's exactly what we want.
6. We want to find __all__ cards. That's why we should know last one. Play with url `https://s1.landingfolio.com/api/v1/inspiration/?offset=0&color=%23undefined`
and find the last offset. In my case its `offset=69`
7. We will get everything in cycle