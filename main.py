import classes


if __name__ == "__main__":
    f = classes.Field(1, 1)

    while True:
        ans = input("Wanna play?(Y/n)")
        if ans == 'Y':
            f.start_game()
            print("Game is started! Print\n",
                  "check\n",
                  "mark\n",
                  "unmark\n")
            f.show_field()
            flag = True

            while flag:

                cmd = input().split()
                x, y = int(cmd[1]), int(cmd[2])
                match cmd[0]:
                    case 'check':
                        f.check(x, y)
                    case 'mark':
                        f.mark(x, y)
                    case 'unmark':
                        f.unmark(x, y)

                is_win: int = f.check_win()
                if is_win == 1:
                    f.end_game(True)
                    flag = False
                elif is_win == -1:
                    f.end_game(False)
                    flag = False
                f.show_field()

        elif ans == 'n':
            break