import pandas as pd
import io

wb = pd.ExcelFile(r"\\to2.to2cz.cz\FS\SOC\05_Testing_all\05_E2E\02 Test analyza\01 E2E kostry (deleni po BUS "
                  r"E2E)\TA_E2E_31_093_JOURNALING_Zadani_pomocny.xlsx")

dfin = wb.parse("rozpad", skiprows=1)

dfin.drop(["Zobrazit v 1P", "Zobrazit ext zákazníkovi", "journaling kategorie", "Event Type\n(filtr pro první úroveň)",
           "Systém", "Event Subtype\n(filtr pro druhou úroveň)", "E2E scénář", "Proces", "Krok v procesu"], 1,
          inplace=True)

atr_list = sorted(
    [(row[0], row[1], ir.replace("\n", "")) for idf, row in dfin.iterrows() for ir, val in row.iteritems() if
     str(val) == "x"], key=lambda x: (x[0].lower(), x[1].lower(), x[2].lower())
)

with io.open(r"D:\temporary indement files\events.txt", "w+", encoding='utf8') as f:
    for tup in atr_list:
        f.write("{}\t{}\t{}\t{} - {}: {}".format(*tup, *tup))
        f.write("\n")
