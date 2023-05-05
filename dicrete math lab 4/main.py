from collections import defaultdict
from math import log2, ceil

#создаем класс элементов дерева для кода хаффмана
class Node:
    def __init__(self, label, weight=0):
        self.label = label
        self.weight = weight
        self.left = None
        self.right = None
        self.code = ""

    #каждый элемент представляется как строка
    def __repr__(self):
        return f"{self.label}: {self.weight}"

#для каждого элемента дерева генерируем код по хаффману
#и сразу закидываем в node.code
def codewords_making(node, code=""):
    if node.left is not None:
        node.left.code = code + "0"
        codewords_making(node.left, code + "0")
    if node.right is not None:
        node.right.code = code + "1"
        codewords_making(node.right, code + "1")


#просто заменяем символы кодами
def encoding(text, codes):
    encoded_text = ""
    for ch in text:
        encoded_text += codes[ch]
    return encoded_text


def encoding_pair(text, codes):
    encoded_text = ""
    for iter in range(1, len(text)-1, 2):
        tmp = text[iter-1] + text[iter]
        encoded_text += codes[tmp]
    return encoded_text


def Shannon_formula(frequencies, text_length):
    shannon = 0
    for char, prob in frequencies.items():
        shannon += (prob / text_length) * log2(prob / text_length)
    return round(-1 * shannon, 6)


# алгоритм Хаффмана

#два словаря где ключи - символы и количество вхождений - значения
freqs1 = defaultdict(int)
freqs2 = defaultdict(int)
text = ""
with open("input.txt", "r") as file:
    text = file.read()
#считаем количество вхождений каждого символа
for ch in text:
    freqs1[ch] += 1
#считаем количество вхождений пар символов
for i in range(0, len(text) - 1):
    freqs2[text[i] + text[i + 1]] += 1

# построение кодов Хаффмана
nodes = []
nodes2 = []

#закидываем элементы в дерево и сортируем по весу - количеству вхождений
for k, v in freqs1.items():
    nodes.append(Node(k, v))
nodes.sort(key=lambda x: x.weight)
end_nodes = nodes.copy()

for k, v in freqs2.items():
    nodes2.append(Node(k, v))
nodes2.sort(key=lambda x: x.weight)
end_nodes2 = nodes2.copy()

#соединяем элементы с наименьшим количеством вхождений в один и суммируем их вес
#затем снова сортируем
#повторяем пока не останется один элемент
while len(nodes) != 1:
    left = nodes.pop(0)
    right = nodes.pop(0)
    node = Node(left.label + right.label, left.weight + right.weight)
    node.left = left
    node.right = right
    nodes.insert(0, node)
    nodes.sort(key=lambda x: x.weight)

while len(nodes2) != 1:
    left = nodes2.pop(0)
    right = nodes2.pop(0)
    node = Node(left.label + right.label, left.weight + right.weight)
    node.left = left
    node.right = right
    nodes2.insert(0, node)
    nodes2.sort(key=lambda x: x.weight)

#теперь создаем словарь где в соответствие каждому элементу ставим его код
codewords_making(nodes[0])
codewords_making(nodes2[0])
codes = dict()
codes_pairs = dict()
for node in end_nodes:
    codes[node.label] = node.code
for node in end_nodes2:
    codes_pairs[node.label] = node.code
encoded = encoding(text, codes)
encoded_pairs = encoding_pair(text, codes_pairs)
freqs1_list = []
freqs2_list = []
for i in freqs1.keys():
    freqs1_list.append([i, freqs1[i]])
for i in freqs2.keys():
    freqs2_list.append([i, freqs2[i]])

#выводим результат
print("Количество символов в исходном тексте: ", len(text))
print("Количество уникальных символов: ", len(freqs1_list), "\n")
with open('output.txt', 'w') as file:
    file.write("Символы и их частоты: " + str(sorted(freqs1_list, key=lambda frequency: frequency[1])))
    file.write("\n\n")
    file.write("Пары символов и их частоты: " + str(sorted(freqs2_list, key=lambda frequency: frequency[1])))
    file.close()
with open('output1.txt', 'w') as file:
    file.write("Символы и их коды Хаффмана: " + str(codes))
    file.write("\n\n")
    file.write("Закодированная строка: " + encoded)
    file.write("\n\n")
    file.write("Пары символов и их коды: " + str(codes_pairs))
    file.write("\n\n")
    file.write("Строка закодированная парами символов: " + encoded_pairs)
    file.close()
print("Длина закодированного текста (метод Хаффмана):", len(encoded))
print("Длина при равномерном (пятибитовом) кодировании:", 5 * len(text))
print("Степень сжатия по сравнению с равномерным (пятибитовым) кодированием:", round(len(encoded)/(5*len(text))*100, 6), "%")
print("Формула Шеннона (метод Хаффмана):", Shannon_formula(freqs1, len(text)), "бит")
print("Кол-во дополнительных бит, требуемых при передаче таблицы для расшифровки:",
      round(len(freqs1_list)*(8+Shannon_formula(freqs1, len(text)))), "\n")

print("Длина текста закодированного через пары символов (метод Хаффмана):", len(encoded_pairs))
print("Степень сжатия по сравнению с равномерным (пятибитовым) кодированием:",
      round((len(encoded_pairs) / (5 * len(text))) * 100, 6), "%")
print("Степень сжатия по сравнению с равномерным кодм Хаффмана для отдельных элементов:",
      round((len(encoded_pairs) / len(encoded)) * 100, 6), "%")
print("Формула Шеннона (метод Хаффмана):", Shannon_formula(freqs2, len(text)), "бит")
print("Кол-во дополнительных бит, требуемых при передаче таблицы для расшифровки:",
      round(len(freqs2_list)*(8+Shannon_formula(freqs2, len(text)))), "\n")

# алгоритм LZW
LZW_dict = dict()
i = 0
#закидываем все одиночные символы в словарь
for char in codes:
    LZW_dict[char] = i
    i += 1
dictionary_size = len(LZW_dict)
#максимальное количество битов
init_bits = ceil(log2(dictionary_size))
string = ""
LZW_encoded = []
#читаем новый символ; если получившаяся строка уже есть в словаре то читаем дальше
#получая при этом новую подстроку
#если нет - добавляем получившуюся в словарь
#каждая новая подстрока кодируется числом равным длине словаря
#новую строку сразу закидываем в lzw_encoded
for char in text:
    new_string = string + char
    if new_string in LZW_dict:
        string = new_string
    else:
        LZW_encoded.append(LZW_dict[string])
        LZW_dict[new_string] = dictionary_size
        dictionary_size += 1
        string = char
if string in LZW_dict:
    LZW_encoded.append(LZW_dict[string])
LZW_encoded_res = ""

#переводим lzw_encoded в двоичный код
for seq in LZW_encoded:
    bits = 0
    if seq == 0:
        bits = init_bits
    elif ceil(log2(seq)) < init_bits:
        bits = init_bits
    else:
        bits = ceil(log2(seq))
    LZW_encoded_res += format(seq, f'0{bits}b')

#выводим результат
with open('output2.txt', 'w') as file:
    file.write("Словарь: " + str(LZW_dict))
    file.write("\n\n")
    file.write("Закодированная строка (битовая): " + LZW_encoded_res)
    file.write("\n\n")
    file.write("Закодированная строка (кодовая): " + str(LZW_encoded))
    file.close()
print()
print("Длина закодированного текста (метод LZW): ", len(LZW_encoded_res))
print("Степень сжатия по сравнению с равномерным (шестибитовым) кодированием:",
      round(100 - (len(LZW_encoded_res) / (6 * len(text))) * 100, 6), "%")
print("Степень сжатия по сравнению с кодами Хаффмана:",
      round(100 - (len(LZW_encoded_res) / len(encoded)) * 100, 6), "%")
