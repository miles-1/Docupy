with open("docs/upmath_readme.md", "w") as f1:
    with open("docs/vscode_readme.md") as f2:
        content = ""
        for line in f2:
            if line.strip() and line.strip()[0] not in ["`", "<"]:
                start = line
                line = line.replace("$", "$$")
                line = line.replace("$$$$", "$$")
                line = line.replace("$$\\sum_i^n", "$$\\textstyle\\sum_i^n")
                indx = line.find("$$")
                if indx != -1 and (indx == 0 or (line[indx - 1] not in ["`", "<", ">"] and line[indx + 3] not in ["`", "<", ">"])):
                    line = line[:indx+2] + "\color{white}" + line[indx+2:]
                line = line.replace("`$$abc$$` for $$math$$", "`$abc$` for $$\\color{white}math$$")
                # if start != line:
                #     print(start.rstrip() + " => " + line)
            f1.write(line)


