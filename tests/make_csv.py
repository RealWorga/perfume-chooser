import csv
import codecs

perfume_names = [
    ["Sauvage Elixir Dior 2021", "Gentleman Eau de Parfym Reserve Privée Givenchy 2022", "Ombré Leather Parfum Tom Form (Unisex) 2021"],
    ["La Nuit de L'Homme Bleu Èlectrique Yves Saint Laurent 2021", "Emporio Armani Stronger With You Absolutely Giorgio Armani 2021", "Dior Homme Original Dior 2021"],
    ["Terre d'Hermes Eau Givree Hermés 2022", "Angels' Share Anniversary Edition By Kilian (unisex) 2022", "Valentino Uomo Intense Valentino 2021"],
    ["Club de Nuit Intense Man Parfum Armaf 2022", "Y Le Parfum Yves Saint Laurent 2021", "The Most Wanted Parfum Azzaro 2022"],
    ["Le Beau Le Parfum Jean Paul Gaultier 2022", "Intense Cedrat Boise Mancera 2021", "Noir Extreme Parfum Tom Ford 2022"],
    ["Acqua di Gió Eau de Parfum Giorgio Armani 2022", "Armani Code Parfum Giorgio Armani 2022", "Dior Homme Sport 2021 ~ 2022"],
    ["Light Blue Forever pour Homme Dolce&Gabbana 2021", "Eros Parfum Versace 2021", "Luna Rossa Ocean Prada 2021"]
]

likeabilities = [
    [3880/2542, 2589/1113, 2460/1181],
    [2197/936, 1989/865, 1817/743],
    [1891/895, 1572/626, 1458/640],
    [1633/1013, 1456/817, 1301/654],
    [1243/751, 1028/458, 983/457],
    [1139/818, 1022/676, 1015/672],
    [900/537, 913/606, 879/543]
]

price_per_ml = [
    [1850/60, 1015/60, 1575/50],
    [950/60, 950/50, 850/50],
    [1040/50, 2330/50, 975/50],
    [404/105, 1275/60, 814/50],
    [885/75, 1380/120, 1575/50],
    [825/40, 905/50, 950/75],
    [835/50, 1430/100, 950/50]
]

perfume_images = [
    ["https://fimgs.net/mdimg/perfume/270x270.68415.jpg", "https://fimgs.net/mdimg/perfume/270x270.71272.jpg", "https://fimgs.net/mdimg/perfume/270x270.68716.jpg"],
    ["https://fimgs.net/mdimg/perfume/270x270.67997.jpg", "https://fimgs.net/mdimg/perfume/270x270.64501.jpg", "https://fimgs.net/mdimg/perfume/270x270.69010.jpg"],
    ["https://fimgs.net/mdimg/perfume/270x270.72439.jpg", "https://fimgs.net/mdimg/perfume/270x270.77132.jpg", "https://fimgs.net/mdimg/perfume/270x270.75094.jpg"],
    ["https://fimgs.net/mdimg/perfume/270x270.72842.jpg", "https://fimgs.net/mdimg/perfume/270x270.64718.jpg", "https://fimgs.net/mdimg/perfume/270x270.73664.jpg"],
    ["https://fimgs.net/mdimg/perfume/270x270.72158.jpg", "https://fimgs.net/mdimg/perfume/270x270.72796.jpg", "https://fimgs.net/mdimg/perfume/270x270.75489.jpg"],
    ["https://fimgs.net/mdimg/perfume/270x270.71606.jpg", "https://fimgs.net/mdimg/perfume/270x270.75126.jpg", "https://fimgs.net/mdimg/perfume/270x270.71326.jpg"],
    ["https://fimgs.net/mdimg/perfume/270x270.66556.jpg", "https://fimgs.net/mdimg/perfume/270x270.70090.jpg", "https://fimgs.net/mdimg/perfume/270x270.68753.jpg"]
]

file = codecs.open('perfume_data.csv', 'w', 'utf-8')
writer = csv.writer(file)
writer.writerow(["Perfume Name", "Likeability", "Price per ml", "Image URL"])
for i in range(len(perfume_names)):
    for j in range(len(perfume_names[0])):
        writer.writerow([perfume_names[i][j], likeabilities[i][j], price_per_ml[i][j], perfume_images[i][j]])
