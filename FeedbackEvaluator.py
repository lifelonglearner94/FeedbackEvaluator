#Feedback Evaluator
import glob
import pandas as pd
import os
import matplotlib.pyplot as plt
import textwrap
from matplotlib.backends.backend_pdf import PdfPages
import pingouin as pg




def readCSVtoPandas():
    # Pfad zum Ordner mit den CSV-Dateien
    ordner_pfad = 'DataInput'

    # Liste aller CSV-Dateien im Ordner
    csv_dateien = glob.glob(f'{ordner_pfad}/*.csv')

    # Sortieren der Dateien nach dem Änderungsdatum (neueste zuerst)
    csv_dateien.sort(key=lambda x: -os.path.getmtime(x))

    # Überprüfen, ob mindestens eine CSV-Datei vorhanden ist
    if csv_dateien:
        # Pfad zur neuesten CSV-Datei
        neueste_csv_datei_pfad = csv_dateien[0]

        # CSV-Datei mit Pandas einlesen
        dataframe = pd.read_csv(neueste_csv_datei_pfad)

        # Den Inhalt des Dataframes anzeigen
        return dataframe
    else:
        print("Keine CSV-Dateien gefunden.")


pandasDataFrameFromInput = readCSVtoPandas()

def makeEvaluationAndCreatePdf(pandasDataFrameFromInput, name):

    def summarizeCategories(pandasDataFrameFromInput):
        result_df = pd.DataFrame()
        
        # Dictionary containing categories and their respective columns
        categories = {
            'Lösungsorientierung': ['Die Person erkennt Probleme effektiv und sucht aktiv nach Lösungen.',
                                    'Die Person zeigt Eigeninitiative bei der Lösung von Herausforderungen.',
                                    'Die Person setzt die Lösungen erfolgreich um.'],
            'Selbstständigkeit': ['Die Person arbeitet selbständig und übernimmt Verantwortung für ihre Aufgaben.',
                                'Die Person kann ohne ständige Anleitung und Aufsicht arbeiten.',
                                'Die Person trifft Entscheidungen und übernimmt erfolgreich Verantwortung.'],
            'Kommunikation': ['Die Person verständigt sich effektiv und tauscht Informationen erfolgreich aus.',
                            'Die Person stellt Fragen, um Missverständnisse zu vermeiden und klare Antworten zu erhalten.',
                            'Die Person hört aktiv zu und nimmt sich Zeit, um andere zu verstehen.'],
            'Teamfähigkeit': ['Die Person ist offen für Ideen und Vorschläge anderer Teammitglieder.',
                            'Die Person teilt ihr Wissen und ihre Erfahrung mit den anderen Teammitgliedern.',
                            'Die Person löst erfolgreich Konflikte und erreicht Konsens.'],
            'Stressresistenz': ['Die Person bewältigt Aufgaben und bleibt effektiv, auch unter Druck oder bei engen Zeitplänen.',
                                'Die Person reagiert schnell auf unvorhergesehene Situationen oder Veränderungen.',
                                'Die Person bleibt auch in stressigen Situationen ruhig und effizient.'],
            'Einfühlungsvermögen': ['Die Person zeigt Verständnis und Mitgefühl für die Bedürfnisse und Gefühle anderer.',
                                'Die Person schafft ein positives und unterstützendes Arbeitsumfeld für andere.',
                                'Die Person versetzt sich erfolgreich in andere hinein und reagiert angemessen.'],
            'Zuverlässigkeit': ['Die Person dokumentiert ihre Arbeit angemessen und hält sich an vereinbarte Prozesse und Verfahren.',
                                'Die Person ist zuverlässig bei der Erledigung von Aufgaben und der Einhaltung von Terminen.',
                                'Die Person erstellt korrekte und vollständige Übergaben oder Dokumentationen.']
        }

        for category, columns in categories.items():
            subset_df_category = pandasDataFrameFromInput[columns]
            try:
                cronbach_alpha_category = pg.cronbach_alpha(subset_df_category)
                print(f"Cronbach's Alpha von {category}:", cronbach_alpha_category)
            except:
                print(f"Berechnung des Cronbach's Alpha nicht möglich für {category}")
            result_df[category] = subset_df_category.mean(axis=1)

        return result_df

    summarizedCategories_df = summarizeCategories(pandasDataFrameFromInput)

    #Gesamtergebnis grafisch darstellen
    ##############################################################################################################################
    # Dein frei wählbarer Text für die erste Seite der PDF
    freier_text = f"Feedback August 2023\n{name}"

    # Mittelwert über alle Spalten berechnen
    mean_values = summarizedCategories_df.mean(numeric_only=True)

    # Absteigend sortieren
    sorted_mean_values = mean_values.sort_values(ascending=False)

    # Standardabweichung für den gesamten DataFrame berechnen
    std_df = summarizedCategories_df.std(numeric_only=True)

    # Umbruch der Balkenbeschriftungen mit textwrap
    wrapped_labels = [textwrap.fill(label, width=10) for label in sorted_mean_values.index]

    # Plot erstellen
    plt.figure(figsize=(8, 6))
    plt.bar(wrapped_labels, sorted_mean_values, yerr=std_df, capsize=5, color='skyblue', edgecolor='black', width=0.6)

    # Achsenbeschriftungen und Titel
    plt.xlabel('Kategorie')
    plt.ylabel('Mittelwerte')
    plt.title('Mittelwerte mit Fehlerbalken (Abweichungen)')
    plt.ylim(1, 5)  # Y-Achse von 1 bis 5

    # Anzeige des Diagramms
    # plt.show()
    ##############################################################################################################################

    # Selbst vs. Fremdwahrnehmung grafisch darstellen
    ##############################################################################################################################
    # Wichtige Spalte zur Unterscheidung von Selbst/Fremdeinschätzung hinzufügen
    summarizedCategories_df['Selbst_Fremd'] = pandasDataFrameFromInput['Beurteilst du dich selbst oder gibst du Feedback?']

    # Werte in der Spalte ändern, damit es im Gesamtkonzept sauber aussieht
    summarizedCategories_df['Selbst_Fremd'] = summarizedCategories_df['Selbst_Fremd'].replace('Feedback geben', 'Fremdeinschätzung')

    # DataFrame nach 'Selbst_Fremd' gruppieren und die Mittelwerte für alle Spalten berechnen
    grouped_df_mean = summarizedCategories_df.groupby('Selbst_Fremd').mean()

    # Balkendiagramm erstellen
    plt.figure()
    grouped_df_mean.plot(kind='bar', rot=0)

    # Diagramm beschriften
    plt.title('Mittelwerte nach Fremd/Selbst')
    plt.xlabel('Fremd/Selbst')
    plt.ylabel('Mittelwerte')

    # y-Achsenbereich setzen (beginnend bei 1)
    plt.ylim(1, 5)

    # Diagramm anzeigen
    # plt.show()
    # Pfad zum gewünschten Ordner
    folder_path = "./output"

    # Überprüfen, ob der Ordner bereits vorhanden ist
    if not os.path.exists(folder_path):
        # Ordner erstellen
        os.makedirs(folder_path)
        print(f"Der Ordner '{folder_path}' wurde erstellt.")
    else:
        print(f"Der Ordner '{folder_path}' ist bereits vorhanden.")

    ##############################################################################################################################
    # PDF erstellen und die Diagramme hinzufügen
    pdf_file = f"output/Feedback_Results_{name}.pdf"
    with PdfPages(pdf_file) as pdf:
        # Erste Seite mit frei wählbarem Text hinzufügen
        plt.figure(figsize=(8, 6))  # Create a new figure for the first page
        plt.text(0.5, 0.5, freier_text, ha='center', va='center', fontsize=16, fontweight='bold')
        plt.axis('off')  # Turn off axis and labels for this page
        pdf.savefig()
        plt.clf()

        # Diagramm 1 hinzufügen (Mittelwerte mit Fehlerbalken)
        plt.figure(figsize=(8, 6))  # Create a new figure for the first plot
        plt.bar(wrapped_labels, sorted_mean_values, yerr=std_df, capsize=5, color='skyblue', edgecolor='black', width=0.6)
        plt.xlabel('Kategorie')
        plt.ylabel('Mittelwerte')
        plt.title('Mittelwerte mit Abweichungslinien')
        plt.ylim(1, 5)
        pdf.savefig()
        plt.clf()

        # Diagramm 2 hinzufügen (Mittelwerte nach Fremd/Selbst)
        plt.figure(figsize=(10, 6))  # Create a new figure for the second plot
        grouped_df_mean.plot(kind='bar', rot=0)
        plt.title('Mittelwerte nach Fremd/Selbst')
        plt.xlabel('Fremd/Selbst')
        plt.ylabel('Mittelwerte')
        # Legende außerhalb des Diagramms platzieren
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.ylim(1, 5)
        # Ändere die Größe der PDF-Seite
        #pdf.infodict()['_pagesize'] = (1200, 600)  # Ändere die Seitenbreite auf 800
        pdf.savefig(bbox_inches='tight')
        plt.clf()

        # Erstelle eine leere Figur und Achsen
        fig, ax = plt.subplots(figsize=(8, 11))  # Hier habe ich die Größe einer A4-Seite gewählt
        # Führe alle TextStrings in einer Variablen zusammen
        combined_text = '\n\n'.join(text for text in pandasDataFrameFromInput['Wohin könnte sich die Person deiner Meinung nach entwickeln, wo liegen ihre Stärken, die sie für zukünftige Aufgaben auszeichnen?'] if text is not None and text.strip() != '')
        # Setze den kombinierten Text auf die Achsen
        ax.text(0, 0.95, "Hinweise zum Entwicklungsplan und Stärken\n(aus Freitextfeld)", ha='left', va='top', fontsize=16, fontweight='bold')
        ax.text(0, 0.84, combined_text, ha='left', va='top', fontsize=12)
        # Entferne Achsenbeschriftungen und Rahmen, um die leere Seite zu erstellen
        ax.axis('off')
        pdf.savefig(fig)



    print(f"Die PDF wurde erstellt: {pdf_file}")
    ##############################################################################################################################