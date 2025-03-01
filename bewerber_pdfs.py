import os
import img2pdf
import pandas as pd

class Konfiguration:
    def __init__(self, excel_pfad, ausgabe_ordner_name="Gruppierte-PDFs"):
        self.excel_pfad = excel_pfad
        self.ausgabe_ordner_name = ausgabe_ordner_name

    def get_excel_pfad(self):
        return self.excel_pfad

    def get_ausgabe_ordner_name(self):
        return self.ausgabe_ordner_name

class ExcelDatenLader:
    def __init__(self, konfiguration):
        self.konfiguration = konfiguration
        self.daten = None

    def lade_excel_daten(self):
        self.daten = pd.read_excel(self.konfiguration.get_excel_pfad())

    def get_daten(self):
        return self.daten

class BewerberGruppierer:
    def __init__(self, daten):
        self.daten = daten

    def gruppiere_nach_bewerber(self):
        return self.daten.groupby("Bewerber")

class PDFErsteller:
    def __init__(self, konfiguration):
        self.konfiguration = konfiguration

    def erstelle_pdf_ordner(self):
        pfad = os.path.join(os.getcwd(), self.konfiguration.get_ausgabe_ordner_name())
        if not os.path.exists(pfad):
            os.makedirs(pfad)
        return pfad

    def konvertiere_und_speichere_pdfs(self, gruppen):
        ordner = self.erstelle_pdf_ordner()
        for bewerber, gruppe in gruppen:
            bildpfade = gruppe["Bild"].tolist()
            ausgabe = os.path.join(ordner, f"{bewerber}.pdf")
            try:
                # Überprüfen, ob alle Bildpfade existieren
                for bildpfad in bildpfade:
                    if not os.path.exists(bildpfad):
                        raise FileNotFoundError(f"Bild nicht gefunden: {bildpfad}")
                
                # PDF erstellen
                with open(ausgabe, "wb") as f:
                    f.write(img2pdf.convert(bildpfade))
                print("PDF erstellt:", ausgabe)
            except Exception as e:
                print("Fehler beim Erstellen von", ausgabe, ":", e)

class Steuerung:
    def __init__(self, excel_pfad):
        self.konfiguration = Konfiguration(excel_pfad)
        self.lader = ExcelDatenLader(self.konfiguration)
        self.pdf_ersteller = PDFErsteller(self.konfiguration)

    def ausfuehren(self):
        self.lader.lade_excel_daten()
        gruppierer = BewerberGruppierer(self.lader.get_daten())
        gruppen = gruppierer.gruppiere_nach_bewerber()
        self.pdf_ersteller.konvertiere_und_speichere_pdfs(gruppen)
        print("Alle Bewerber-PDFs wurden erstellt.")

if __name__ == "__main__":
    pfad = "/Users/a9119/Desktop/Neuer Ordner/Excel/Bewerber.xlsx"  # Pfad zur Excel-Datei
    steuerung = Steuerung(pfad)
    steuerung.ausfuehren()