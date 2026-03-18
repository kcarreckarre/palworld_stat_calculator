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
                const skills = [];
                const skillElements = document.querySelectorAll("#__nuxt > div > section > div.container > div.right > div.abilities > div.active.skills > div > div");

                skillElements.forEach((_, index) => {
                    const nameElem = document.querySelector(`#\\__nuxt > div > section > div.container > div.right > div.abilities > div.active.skills > div > div:nth-child(${index + 1}) > div.header > div.wrap > div.name`);
                    const elementElem = document.querySelector(`#\\__nuxt > div > section > div.container > div.right > div.abilities > div.active.skills > div > div:nth-child(${index + 1}) > div.header > div.waza-element > div > img`);
                    const powerElem = document.querySelector(`#\\__nuxt > div > section > div.container > div.right > div.abilities > div.active.skills > div > div:nth-child(${index + 1}) > div.stats > div > div.item.red > div.value`);
                    const cooldownElem = document.querySelector(`#\\__nuxt > div > section > div.container > div.right > div.abilities > div.active.skills > div > div:nth-child(${index + 1}) > div.stats > div > div.item.yellow > div.value`);
                    const rangeElem = document.querySelector(`#\\__nuxt > div > section > div.container > div.right > div.abilities > div.active.skills > div > div:nth-child(${index + 1}) > div.stats > div > div.item.grey > div.value`);

                    const name = nameElem ? nameElem.textContent.trim() : null;
                    const element = elementElem ? elementElem.getAttribute('src') : null;
                    const power = powerElem ? powerElem.textContent.trim() : null;
                    const cooldown = cooldownElem ? cooldownElem.textContent.trim() : null;
                    const range = rangeElem ? rangeElem.textContent.trim() : null;

                    if (name) {
                        skills.push({
                            name,
                            element,
                            power,
                            cooldown,
                            range
                        });
                    }
                });

                return { skills };
            });

            data.push({ name: pal, ...palData });
            console.log(`Scraped data for: ${pal}`);
        } catch (error) {
            console.error(`Failed to scrape data for: ${pal}, Error: ${error}`);
        }
    }

    await browser.close();

    fs.writeFileSync('pals_skill_details.json', JSON.stringify(data, null, 2));
    console.log('Data saved to pals_skill_details.json');
})();












