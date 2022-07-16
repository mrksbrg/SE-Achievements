# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2021

@author: Markus Borg
"""

import sys
import os.path
from datetime import date
import xml.sax
import ssl
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator
#from swesesci.scholar_visualizer import ScholarVisualizer

sss_scholars = []
sss_affiliations = []

def url_splitter(scholar_string):
    name = scholar_string[0]
    running_number = scholar_string[1]
    url = scholar_string[2]

    try:
        split1 = url.split("pid/")
        split2 = split1[1].split(".xml")
        pid = split2[0]
    except IndexError:
        print("Invalid format of input XML URL. (" + name + ")")
        return

    return (name, running_number, pid, url)

def fp_add_sss_scholars(candidate_scholars, affiliation):
    result = list(map(url_splitter, candidate_scholars))
    print(result)

def add_sss_scholars(process_list, affiliation):
    for person in process_list:
        name = person[0]
        running_number = person[1]
        url = person[2]
        # extract the pid from the url by substringing
        try:
            split1 = url.split("pid/")
            split2 = split1[1].split(".xml")
            pid = split2[0]
        except IndexError:
            print("Invalid format of input XML URL. (" + name + ")")
            return

        sss_scholars.append(SSSScholar(name, running_number, pid, url, affiliation, -1))
        tmp_aff = SSSAffiliation(affiliation)
        if tmp_aff not in sss_affiliations:
            tmp_aff.nbr_scholars += 1
            sss_affiliations.append(tmp_aff)
        else:
            curr = next((x for x in sss_affiliations if affiliation == x.name), None)
            curr.nbr_scholars += 1

# Swe-SE-SCI entry point
if (len(sys.argv) == 1):
    #test_list = [("Stefan Cedergren", "-1", "https://dblp.org/pid/116/6013.xml")]
    #add_sss_scholars(test_list, "Fast test")
    rise_list = [("Niklas Mellegård", "-1", "https://dblp.org/pid/30/8216.xml"),
                 ("Efi Papatheocharous", "-1", "https://dblp.org/pid/76/302.xml"),
                 ("Mehrdad Saadatmand", "-1", "https://dblp.org/pid/14/9944.xml"),
                 ("Pasqualina Potena", "-1", "https://dblp.org/pid/49/2251.xml"),
                 ("Markus Borg", "-1", "https://dblp.org/pid/47/9384.xml"),
                 ("Ulrik Franke", "-1", "https://dblp.org/pid/71/3754.xml"),
                 ("Maria Ulan", "-1", "https://dblp.org/pid/221/1630.xml"),
                 ("Jakob Axelsson", "-1", "https://dblp.org/pid/50/6797.xml"),
                 ("Håkan Burden", "-1", "https://dblp.org/pid/02/10779.xml"),
                 ("Peter Wallin", "-1", "https://dblp.org/pid/57/5749.xml"),
                 ("Piotr Tomaszewski", "-1", "https://dblp.org/pid/75/5273.xml"),
                 ("Thomas Olsson", "0001", "https://dblp.org/pid/31/5587-1.xml"),
                 ("Kenneth Lind", "-1", "https://dblp.org/pid/46/7676.xml"),
                 ("Paris Carbone", "-1", "https://dblp.org/pid/90/7704.xml"),
                 ("Terese Besker", "-1", "https://dblp.org/pid/187/7364.xml")]
    lu_list = [("Per Runeson", "-1", "https://dblp.org/pid/24/24.xml"),
               ("Björn Regnell", "-1", "https://dblp.uni-trier.de/pid/09/1284.xml"),
               ("Martin Höst", "-1", "https://dblp.uni-trier.de/pid/07/6594.xml"),
               ("Elizabeth Bjarnason", "-1", "https://dblp.uni-trier.de/pid/19/1459.xml"),
               ("Emelie Engström", "-1", "https://dblp.uni-trier.de/pid/31/2107.xml"),
               ("Christin Lindholm", "-1", "https://dblp.uni-trier.de/pid/20/851.xml"),
               ("Christoph Reichenbach", "-1", "https://dblp.uni-trier.de/pid/98/4527.xml"),
               ("Görel Hedin", "-1", "https://dblp.uni-trier.de/pid/95/987.xml"),
               ("Martina Maggio", "-1", "https://dblp.uni-trier.de/pid/02/8575.xml")]
    bth_list = [("Claes Wohlin", "-1", "https://dblp.org/pid/w/ClaesWohlin.xml"),
                ("Tony Gorschek", "-1", "https://dblp.org/pid/82/3504.xml"),
                ("Krzysztof Wnuk", "-1", "https://dblp.org/pid/86/2856.xml"),
                ("Michael Unterkalmsteiner", "-1", "https://dblp.org/pid/08/8212.xml"),
                ("Michael Mattsson", "-1", "https://dblp.org/pid/04/6269.xml"),
                ("Mikael Svahnberg", "-1", "https://dblp.org/pid/81/5477.xml"),
                ("Darja Smite", "-1", "https://dblp.org/pid/30/4138.xml"),
                ("Jürgen Börstler", "-1", "https://dblp.org/pid/b/JBorstler.xml"),
                ("Emil Alégroth", "-1", "https://dblp.org/pid/133/4686.xml"),
                ("Nauman Bin Ali", "-1", "https://dblp.org/pid/37/10608.xml"),
                ("Fabian Fagerholm", "-1", "https://dblp.org/pid/78/9972.xml"),
                ("Javier Gonzalez-Huerta", "-1", "https://dblp.org/pid/98/8522.xml"),
                ("Muhammad Usman", "0006", "https://dblp.org/pid/20/241-6.xml"),
                ("Davide Fucci", "-1", "https://dblp.org/pid/70/9016.xml"),
                ("Daniel Méndez Fernández", "-1", "https://dblp.org/pid/69/8522.xml"),
                ("Deepika Badampudi", "-1", "https://dblp.org/pid/130/6487.xml"),
                ("Emilia Mendes", "-1", "https://dblp.org/pid/m/EMendes.xml"),
                ("Ludwik Kuzniarz", "-1", "https://dblp.org/pid/26/532.xml"),
                ("Lars Lundberg", "-1", "https://dblp.org/pid/58/356.xml"),
                ("Niklas Lavesson", "-1", "https://dblp.org/pid/55/1994.xml"),
                ("Ahmad Nauman Ghazi", "-1", "https://dblp.org/pid/156/2314.xml"),
                ("Binish Tanveer", "-1", "https://dblp.org/pid/180/0071.xml"),
                ("Eriks Klotins", "-1", "https://dblp.org/pid/163/6012.xml")]
    chalmers_list = [("Philipp Leitner", "0001", "https://dblp.org/pid/03/5268.xml"),
                     ("Rogardt Heldal", "-1", "https://dblp.org/pid/70/2264.xml"),
                     ("Patrizio Pelliccione", "-1", "https://dblp.org/pid/p/PatrizioPelliccione.xml"),
                     ("Miroslaw Staron", "-1", "https://dblp.org/pid/16/5647.xml"),
                     ("Jan-Philipp Steghöfer", "-1", "https://dblp.org/pid/16/7127.xml"),
                     ("Robert Feldt", "-1", "https://dblp.org/pid/97/831.xml"),
                     ("Richard Torkar", "-1", "https://dblp.org/pid/52/972.xml"),
                     ("Richard Berntsson-Svensson", "-1", "https://dblp.org/pid/08/1588.xml"),
                     ("Francisco Gomes de Oliveira Neto", "-1", "https://dblp.org/pid/56/1704.xml"),
                     ("Gregory Gay", "-1", "https://dblp.org/pid/39/7539.xml"),
                     ("Jan Bosch", "-1", "https://dblp.org/pid/60/6845.xml"),
                     ("Jennifer Horkoff", "-1", "https://dblp.org/pid/92/5983.xml"),
                     ("John Hughes", "-1", "https://dblp.org/pid/h/JohnHughes.xml"),
                     ("Eric Knauss", "-1", "https://dblp.org/pid/k/EricKnauss.xml"),
                     ("Regina Hebig", "-1", "https://dblp.org/pid/63/9280.xml"),
                     ("Agneta Nilsson", "-1", "https://dblp.org/pid/18/4800.xml"),
                     ("Imed Hammouda", "-1", "https://dblp.org/pid/14/5303.xml"),
                     ("Birgit Penzenstadler", "-1", "https://dblp.org/pid/92/3113.xml"),
                     ("Lars Pareto", "-1", "https://dblp.org/pid/p/LarsPareto.xml"),
                     ("Christian Berger", "0001", "https://dblp.org/pid/98/4996-1.xml"),
                     ("Daniel Strüber", "0001", "https://dblp.org/pid/46/11388-1.xml")]
    mdh_list = [("Alessio Bucaioni", "-1", "https://dblp.org/pid/143/4024.xml"),
                ("Luciana Provenzano", "-1", "https://dblp.org/pid/35/160.xml"),
                ("Hans A. Hansson", "-1", "https://dblp.org/pid/65/1154.xml"),
                ("Jan Carlsson", "-1", "https://dblp.org/pid/98/10376.xml"),
                ("Antonio Cicchetti", "-1", "https://dblp.org/pid/28/2455.xml"),
                ("Federico Ciccozzi", "-1", "https://dblp.org/pid/36/10028.xml"),
                ("Séverine Sentilles", "-1", "https://dblp.org/pid/38/7036.xml"),
                ("Kristina Lundqvist", "-1", "https://dblp.org/pid/53/2238.xml"),
                ("Daniel Sundmark", "-1", "https://dblp.org/pid/98/7045.xml"),
                ("Wasif Afzal", "-1", "https://dblp.org/pid/59/5422.xml"),
                ("Eduard Paul Enoiu", "-1", "https://dblp.org/pid/119/1657.xml"),
                ("Barbara Gallina", "-1", "https://dblp.org/pid/34/3823.xml"),
                ("Mikael Sjödin", "-1", "https://dblp.org/pid/37/6301.xml"),
                ("Daniel Flemström", "-1", "https://dblp.org/pid/13/6886.xml"),
                ("Saad Mubeen", "-1", "https://dblp.org/pid/80/8239.xml"),
                ("Cristina Cerschi Seceleanu", "-1", "https://dblp.org/pid/85/2148.xml")]
    kth_list = [("Martin Monperrus", "-1", "https://dblp.org/pid/62/5292.xml"),
                ("Frederic Loiret", "-1", "https://dblp.org/pid/17/1176.xml"),
                ("Karl Meinke", "-1", "https://dblp.org/pid/70/1381.xml"),
                ("Benoit Baudry", "-1", "https://dblp.org/pid/57/3320.xml"),
                ("Pontus Johnson", "-1", "https://dblp.org/pid/79/6862.xml"),
                ("Robert Lagerström", "-1", "https://dblp.org/pid/53/3982.xml"),
                ("Mathias Ekstedt", "-1", "https://dblp.org/pid/23/402.xml"),
                ("Martin Törngren", "-1", "https://dblp.org/pid/95/1411.xml"),
                ("Hannes Holm", "-1", "https://dblp.org/pid/77/9017.xml"),
                ("Cyrille Artho", "-1", "https://dblp.org/pid/21/6330.xml"),
                ("Mira Kajko-Mattsson", "-1", "https://dblp.org/pid/20/0.xml"),
                ("Philipp Haller", "-1", "https://dblp.org/pid/94/5786.xml"),
                ("David Broman", "-1", "https://dblp.org/pid/13/3318.xml"),
                ("Elena Troubitsyna", "-1", "https://dblp.org/pid/84/4265.xml"),
                ("Richard Glassey", "-1", "https://dblp.org/pid/00/4905.xml"),
                ("Musard Balliu", "-1", "https://dblp.org/pid/25/7796.xml"),
                ("Fredrik Asplund", "-1", "https://dblp.org/pid/34/9961.xml")]
    su_list = [("Janis Stirna", "-1", "https://dblp.org/pid/86/5210.xml"),
               ("Jelena Zdravkovic", "-1", "https://dblp.org/pid/32/855.xml"),
               ("Martin Henkel", "-1", "https://dblp.org/pid/88/250.xml"),
               ("Erik Perjons", "-1", "https://dblp.org/pid/97/6128.xml")]
    # Emeritus "Ilia Bider", "-1", "https://dblp.org/pid/27/111.xml"
    malmo_list = [("Helena Holmström Olsson", "-1", "https://dblp.org/pid/71/1008.xml"),
                  ("Patrik Berander", "-1", "https://dblp.org/pid/99/2602.xml"),
                  ("Carl Magnus Olsson", "-1", "https://dblp.org/pid/27/4256.xml"),
                  ("Jeanette Eriksson", "-1", "https://dblp.org/pid/18/5227.xml"),
                  ("Bahtijar Vogel", "-1", "https://dblp.org/pid/96/8481.xml"),
                  ("Hussan Munir", "-1", "https://dblp.org/pid/124/2690.xml")]
    linkoping_list = [("Kristian Sandahl", "-1", "https://dblp.org/pid/59/4490.xml"),
                      ("Peter Fritzson", "-1", "https://dblp.org/pid/f/PeterFritzson.xml"),
                      ("Mariam Kamkar", "-1", "https://dblp.org/pid/k/MariamKamkar.xml"),
                      ("Ola Leifler", "-1", "https://dblp.org/pid/11/3334.xml")]
    linne_list = [("Jesper Andersson", "-1", "https://dblp.org/pid/49/6212.xml"),
                  ("Morgan Ericsson", "-1", "https://dblp.org/pid/11/565.xml"),
                  ("Narges Khakpour", "-1", "https://dblp.org/pid/72/7537.xml"),
                  ("Welf Löwe", "-1", "https://dblp.org/pid/l/WelfLowe.xml"),
                  ("Francesco Flammini", "-1", "https://dblp.org/pid/f/FrancescoFlammini.xml"),
                  ("Francis Palma", "-1", "https://dblp.org/pid/34/10082.xml"),
                  ("Andreas Kerren", "-1", "https://dblp.org/pid/44/6743.xml"),
                  ("Rafael Messias Martins", "-1", "https://dblp.org/pid/117/2529.xml"),
                  ("Anna Wingkvist", "-1", "https://dblp.org/pid/55/7247.xml"),
                  ("Jonas Lundberg", "-1", "https://dblp.org/pid/86/5187.xml"),
                  ("Mauro Caporuscio", "-1", "https://dblp.org/pid/c/MauroCaporuscio.xml"),
                  ("Diego Perez-Palacin", "-1", "https://dblp.org/pid/26/7841.xml")]
    skovde_list = [("Björn Lundell", "-1", "https://dblp.org/pid/37/6147.xml"),
                   ("Sten Andler", "-1", "https://dblp.org/pid/a/StenFAndler.xml"),
                   ("Birgitta Lindström", "-1", "https://dblp.org/pid/89/4385.xml"),
                   ("Henrik Gustavsson", "-1", "https://dblp.org/pid/19/2531.xml"),
                   ("Jonas Gamalielsson", "-1", "https://dblp.org/pid/95/49.xml"),
                   ("Simon Butler", "0001", "https://dblp.org/pid/96/7675-1.xml"),
                   ("Joeri van Laere", "-1", "https://dblp.org/pid/17/312.xml"),
                   ("Anne Persson", "-1", "https://dblp.org/pid/45/5030.xml"),
                   ("Beatrice Alenljung", "-1", "https://dblp.org/pid/83/4149.xml"),
                   ("Jeremy Rose", "-1", "https://dblp.org/pid/29/3118.xml")]
    karlstad_list = [("Sebastian Herold", "-1", "https://dblp.org/pid/23/6842.xml"),
                     ("Bestoun S. Ahmed", "-1", "https://dblp.org/pid/60/2757.xml"),
                     ("Martin Blom", "-1", "https://dblp.org/pid/24/3713.xml"),
                     ("Muhammad Ovais Ahmad", "-1", "https://dblp.org/pid/143/1116.xml")]
    jonkoping_list = [("Anders Adlemo", "-1", "https://dblp.org/pid/65/4551.xml")]
    orebro_list = [("Panagiota Chatzipetrou", "-1", "https://dblp.org/pid/09/10404.xml"),
    			   ("Fredrik Karlsson", "0001", "https://dblp.org/pid/54/4340.xml")]
    halmstad_university = [("Walid Taha", "-1", "https://dblp.org/pid/53/5525.xml")]
    university_west = [("Annabella Loconsole", "-1", "https://dblp.org/pid/69/4553.xml")]

    #add_sss_scholars(rise_list, "RISE Research Institutes of Sweden")
    #add_sss_scholars(lu_list, "Lund University")
    #add_sss_scholars(bth_list, "Blekinge Institute of Technology")
    #add_sss_scholars(chalmers_list, "Chalmers / Gothenburg University")
    #add_sss_scholars(mdh_list, "Mälardalen University")
    #add_sss_scholars(kth_list, "KTH Royal Institute of Technology")
    #add_sss_scholars(su_list, "Stockholm University")
    #add_sss_scholars(malmo_list, "Malmö University")
    fp_add_sss_scholars(malmo_list, "Malmö University")
    #add_sss_scholars(linkoping_list, "Linköping University")
    #add_sss_scholars(linne_list, "Linneaus Univerity")
    #add_sss_scholars(skovde_list, "Skövde University")
    #add_sss_scholars(karlstad_list, "Karlstad University")
    #add_sss_scholars(jonkoping_list, "Jönköping University")
    #add_sss_scholars(orebro_list, "Örebro University")
    #add_sss_scholars(halmstad_university, "Halmstad University")
    #add_sss_scholars(university_west, "University West")

# Process scholar provided in the argument
else:
    specific_scholar = (sys.argv[1], sys.argv[2], sys.argv[3])
    custom_list = []
    custom_list.append(specific_scholar)
    add_sss_scholars(custom_list, "N/A")

# Prepare the process
subdirectory = "output"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

# 1. Mine the scholars, write the results
print("####### Step 1 - Mining scholars #######")
parser = xml.sax.make_parser()
# turn off namespaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
miner = ScholarMiner(filename_prefix, sss_scholars, sss_affiliations)
ssl._create_default_https_context = ssl._create_unverified_context
miner.parse_scholars()
miner.write_results()
sss_scholars = miner.get_scholars()

# 2. Analyze the scholars, remove affiliations with no first-authored SCI publications, write the results
print("\n####### Step 2 - Analyzing scholars #######")
for scholar in sss_scholars:
    curr = next((x for x in sss_affiliations if scholar.affiliation == x.name), None)
    curr.nbr_first_sci += scholar.nbr_first_sci
tmp_affiliations = []
for affiliation in sss_affiliations:
    # keep only affiliations with SSS scholars
    if affiliation.nbr_first_sci > 0:
        tmp_affiliations.append(affiliation)
sss_affiliations = tmp_affiliations
analyzer = ScholarAnalyzer(filename_prefix, sss_scholars, sss_affiliations)
analyzer.analyze_individual_research_interests()
analyzer.analyze_affiliation_topics()
analyzer.write_results()

# 3. Tabulate the scholars, write the results
print("\n####### Step 3 - Tabulating scholars #######")
sss_scholars.sort(reverse=True)
sss_affiliations.sort(reverse=True)
tabulator = ScholarTabulator(filename_prefix, sss_scholars, sss_affiliations)
tabulator.write_tables()

# 4. Visualize the results, save to files
#visualizer = ScholarVisualizer(filename_prefix)
