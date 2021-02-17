string1 = "  UPC Coded: No,  Case of: 36,  How packaged: 36 Pieces per Case,"
string2 = "Wreath is perfect for decorating doorways, windows, staircases, lamp posts, garage doors. ,  Case Dimensions: 13.38 inches (Length) X 13.38 inches (Width) X 12.2 inches (Height),  UPC Coded: No,  Case of: 24,  How packaged: 24 Pieces per Case,"
string3 = 'a normal string'
string4 = "Our Sunshade protects your car interior from hot weather. This helps with reducing some heat, and keeps your interior looking new. , WARNING: Cancer and Reproductive Harm - , www.P65Warnings.ca.gov.,  Case Dimensions: 26 inches Item Length (inches) X 27 inches Item Height (inches) X 15 inches Item Width (inches),  UPC Coded: Yes,  Case of: 48,  How packaged: 48 Packs per Case,"
string5 = "BAZIC Magnetic Whiteboard Eraser w Foam Comfort Grip Made of Lightweight contoured foam for a more comfortable grip ,  Case Dimensions: 20.5 inches (Length) X 10.5 inches (Width) X 15 inches (Height),  UPC Coded: Yes: 764608022412,  Case of: 24,  How packaged: 24 Pieces per CASE,"
def upc_avail(string):
    index = string.rfind('UPC')
    if index<0:
        upc = ''
        return upc
    else:
        new_string = string[index:]
        comma_index = new_string.find(',')
        upc = new_string[:comma_index]
        if upc == 'UPC Coded: No':
            return upc
        else:
            return 'UPC Coded: Yes'
upc_1 = ''
upc_2 = 'UPC Coded: No'
upc_3 = 'UPC Coded: Yes'
upc_4 = 'UPC Coded: Yes: 764608022412'


def upc_code(string):
    if string == '' or string == 'UPC Coded: No' or string == 'UPC Coded: Yes':
        return ''
    else:
        index = string.rfind(':')
        code = string[index+1:]
        return code.strip()



price_2 = '$207.36'
price_3 = '$1.44/pcx144pcs=$207.36'
def min_price(string):
    equal_index = string.rfind('=')
    if equal_index<0:
        price = string.strip(',')
        return price
    mul_index = string.find('x')
    return string[:mul_index]

price = min_price(price_3)
    
print(price)

