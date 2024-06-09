const puppeteer = require('puppeteer');
const fs = require('fs');

const pals_list = [
    "Frostallion", "Jetragon", "Paladius", "Necromus", "Bellanoir",
    "Anubis", "Grizzbolt", "Jormuntide", "Suzaku", "Elphidran Aqua",
    "Relaxaurus", "Kingpaca", "Menasting", "Blazamut", "Orserk",
    "Incineram", "Lunaris", "Pyrin", "Robinquill", "Kitsun",
    "Mossanda", "Foxcicle", "Nitewing", "Mau", "Rushoar",
    "Galeclaw", "Jolthog", "Bristla", "Hangyu", "Leezpunk",
    "Fuack", "Sparkit", "Kelpsea", "Killamari", "Flopie",
    "TanZee", "Ribbuny", "Flambelle", "Daedream", "Depresso",
    "Teafant", "Direhowl", "Bushi", "Grintale", "Rayhound",
    "Wumpo Botan", "Tombat", "Dinossom", "Felbat", "Cinnamoth"
];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const data = [];

    for (const pal of pals_list) {
        try {
            const formattedPalName = pal.replace(/\s+/g, '-').toLowerCase();
            const url = `https://palworld.gg/pal/${formattedPalName}`;
            await page.goto(url, { waitUntil: 'domcontentloaded' });

            const palData = await page.evaluate(() => {
                const imgElem = document.querySelector("#__nuxt > div > section > div.pal > div.image > img");
                const hpElem = document.querySelector("#__nuxt > div > section > div.container > div.left > div.stats > div > div:nth-child(1) > div.value");
                const defenseElem = document.querySelector("#__nuxt > div > section > div.container > div.left > div.stats > div > div:nth-child(2) > div.value");
                const attackElem = document.querySelector("#__nuxt > div > section > div.container > div.left > div.stats > div > div:nth-child(5) > div.value");

                const img_src = imgElem ? imgElem.src : null;
                const hp = hpElem ? hpElem.textContent.trim() : null;
                const defense = defenseElem ? defenseElem.textContent.trim() : null;
                const attack = attackElem ? attackElem.textContent.trim() : null;

                return {
                    img_src,
                    hp,
                    defense,
                    attack
                };
            });

            data.push({ name: pal, ...palData });
            console.log(`Scraped data for: ${pal}`);
        } catch (error) {
            console.error(`Failed to scrape data for: ${pal}, Error: ${error}`);
        }
    }

    await browser.close();

    fs.writeFileSync('pals_data.json', JSON.stringify(data, null, 2));
    console.log('Data saved to pals_data.json');
})();


