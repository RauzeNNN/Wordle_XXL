from random import choice


# Taking words as a list.
def words(file_name):
    file = open(file_name, "r")
    arr = []
    for i in file:
        arr.append(i.lower().rstrip("\n"))
    file.close()
    return arr


# Controlling the guessed word and computing which color should every letter be.
# For  better understanding, examine wordle rules.
def control_word(asked, guess):
    # 0 = grey , 1 = yellow, 2 = green
    arr = [0, 0, 0, 0, 0]

    asked_arr = []
    for i in asked:
        asked_arr.append(i)

    guess_arr = []
    for j in guess:
        guess_arr.append(j)

    temp = asked_arr[:]
    for a in range(len(asked_arr)):
        if guess_arr[a] == asked_arr[a]:
            arr[a] = 2
            temp.remove(asked_arr[a])

    for k in range(len(asked_arr)):
        if arr[k] != 2:
            if guess_arr[k] in temp:
                arr[k] = 1
                temp.remove(guess_arr[k])

    return arr


# For printing colored line according to list which is created from control_word()
def colorizer(arr):
    res = ""
    for i in arr:
        if i == 2:
            res = res + "🟩"
        elif i == 1:
            res = res + "🟨"
        elif i == 0:
            res = res + "⬜"
        else:
            raise Exception("list error.")
    print(res)


# Finds letter which is not included in word and adds them on a list.
def add_missed_letters(non_inc, word, arr, num):
    ctrl = [[], [], []]     # first one zeros last one twos
    for x in range(len(arr)):
        if arr[x] == 0:
            ctrl[0].append(word[x])
        elif arr[x] == 1:
            ctrl[1].append(word[x])
        elif arr[x] == 2:
            ctrl[2].append(word[x])
    for i in range(len(arr)):
        if arr[i] == 0 and word[i] not in non_inc[num] and word[i] not in ctrl[1] and word[i] not in ctrl[2]:
            non_inc[num].append(word[i])


def main():
    words_arr = words("kelimeler.txt")
    non_included_words = []
    asked = []
    is_done = []
    not_finished = True

    try:
        w_count = int(input("Aynı anda kaç kelimeyi çözmek istiyorsun? : "))
    except:
        x = input("Tam sayı girmelisin!: ")
        while not x.isdigit():
            x = input("Tam sayı girmelisin!: ")
        w_count = int(x)

    for x in range(w_count):
        asked.append(choice(words_arr))
        non_included_words.append([])
        is_done.append(0)

    count = w_count + 5
    while count > 0 and not_finished:
        print(f"{count} deneme hakkın var.")
        guess = input("Tahmin: ").lower()

        while guess not in words_arr:
            print("Veritabanında böyle bir kelime yok.")
            guess = input("Tahmin: ").lower()

        for i in range(w_count):
            if is_done[i] == 0:
                arr = control_word(asked[i], guess)
                print(f"{i+1}.")
                colorizer(arr)
                add_missed_letters(non_included_words, guess, arr, i)
                print("Olmayan harfler: " + "".join(sorted(non_included_words[i])))

                if asked[i] == guess:
                    is_done[i] = 1
                if 0 not in is_done:
                    not_finished = False
                    break
        count -= 1

    if count == 0:
        print(f"Kaybettin. Kelimelerin: {asked}")
    else:
        print("Tebrikler, Kazandın!")


if __name__ == "__main__":
    main()
