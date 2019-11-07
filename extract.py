import sys
import csv
import re

#COLORS DATA MUST BE EXTENDED AS FAR AS POSSIBLE (OR REPLACED WITH REG)
color_map = {
    'жёлтый' : 'YELLOW',
    'жёлт.' : 'YELLOW',

    'рубиново-красный': 'RED',
    'рубиново-красные': 'RED',
    'Красное вино': 'RED',
    'темно-красные': 'RED',
    'красный': 'RED',
    'RAL-3005': 'RED',
    'RAL 3005': 'RED',

    'шоколадно-коричневый': 'BROWN',
    'земельно-коричневый': 'BROWN',
    'темно-коричневый': 'BROWN',
    'коричневый шоколад': 'BROWN',
    'коричневый': 'BROWN',
    'RAL 8017': 'BROWN',
    'RAL-8017': 'BROWN',

    'RAL 7004' : 'GRAY',

    'т-зеленый' : 'GREEN',
    'зеленый насыщенный' : 'GREEN',
    'зеленый' : 'GREEN',
    'RAL-6020' : 'GREEN',

    'бел.' : 'WHITE',
    'Белый' : 'WHITE',
    'белый' : 'WHITE',
    'RAL 9003' : 'WHITE',
    'RAL-9003' : 'WHITE',
    
    'синяя вода' : 'BLUE',
    'небесно-голубой' : 'BLUE',
    'ультрамарин синий' : 'BLUE',
    'ультрамарин' : 'BLUE',
    'синий насыщенный' : 'BLUE',
    'ярко-синий' : 'BLUE',
    'синий' : 'BLUE',
    'RAL-5005' : 'BLUE',
    'RAL-5021' : 'BLUE',

    'черн.' : 'BLACK',
    'чёрн.' : 'BLACK',
    'чёрный' : 'BLACK',
    'чёрные' : 'BLACK',
    'RAL-9005' : 'BLACK',
}

garbage_list = ["тов", "промо", "цвет", "мм", "кг", "шт", "[^а-яА-Яa-zA-Z-]", " +", "-+"]

def find_size(data):
    rrr = r"[0-9]?[',','.']?[0-9]\s*['х','x','/','*']\s*[0-9]?[',','.']?[0-9]?[0-9]"
    size = re.findall(rrr, data)

    if len(size) > 0:
        sizes = re.split(r"['х','x','/','*']", size[0])
        length, diameter = float(sizes[0]), float(sizes[1])
    else:
        length, diameter = 0.0, 0.0 #USING FLOAT FOR UNDEFINED VALUE POTENTIALLY PROVIDES COMPATIBILITY

    data_no_size = re.sub(rrr, '', data, 1)
    return data_no_size, length, diameter

def find_color(data):
    colors_checks_max = 3 #GREATER NUMBER FOR GREATER ACCURACY OF FINDING SYNONYMS, BUT REDUCES PERFORMANCE
    colors_checks = 0

    color_str = 'UNDEFINED'

    for color in color_map:
        if data.find(color) != -1:
            colors_checks += 1
            data = data.replace(color, '')
            color_str = color_map[color]

            if colors_checks >= colors_checks_max:
                return data, color

    return data, color_str

def clear_garbage(data):
    for garbage in garbage_list:
        data = re.sub(garbage, ' ', data)

    return data.rstrip()

def main():
    print ("Parsing", sys.argv[1])
    temp = []

    try:
        with open(sys.argv[1], encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = row['title']
                data, length, diameter = find_size(data)
                data, color = find_color(data)
                #OPTIONAL FOR GETTING PRODUCT NAME
                #data = clear_garbage(data)
                
                temp.append({
                    'id':row['id'],
                    'length':length,
                    'diameter':diameter,
                    'color':color,
                })

        csvfile.close()
        
        with open('out-attributes.csv', 'w', newline='\n', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'length', 'diameter', 'color']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for line in temp:
                writer.writerow(line)

        csvfile.close()

    except IOError as e:
        print("File error (%s)." % e)

if __name__ == '__main__':
    main()