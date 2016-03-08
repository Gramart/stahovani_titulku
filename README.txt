ISJ 2014 - automaticke stahovani a srovnavani titulku k filmum
Autor: Martin Graca, xgraca00, 1BIT
Vytvoreno: duben 2014, Python verze 2.7.4
Popis: Skript stahne ceske titulky, defaultne ze zadaneho url nebo na zaklade nazvu filmu nebo imdb identifikatoru. Pote stahne nejnovejsi anglicke titulky. Nakonec skript zarovna ceske a anglicke titulky podle casoveho okna +- 0.5s.

pouzite moduly: datetime - pro praci s casem titulku, xml.etree.ElementTree - parsovani xml stranky, zipfile - odzipovani stazenych titulku

Pouziti programu:
 ./titulky.py [DOWNLOAD_LINK][-a] [-i IMDB_ID]|[-m MOVIE] [-d]
 -a: se zadanym argumentem -a skript stahne vsechny dostupne anglicke titulky, pote porovnava vsechny stazene titulky a do souboru out.txt ulozi zarovnavni s nejvyssi shodou. Toto vicenasobne porovnavani je vsak pomerne casove narocne, cca 25s jedno porovnani.
-i: IMDB_ID je identifikator ceskeho filmu, podle ktereho skript stahne ceske tititulky
-m: MOVIE je nazev ceskeho filmu, podle ktereho skript nalezne ceske titulky

out.txt: vystupni soubor skriptu ve formatu:
					    ceska_promluva /t anglicka_promluva
            pokud chybi ceska promluva:			   /t anglicka_promluva
	    pokud chybi anglicka promluva:  ceska_promluva /t
-d: se zadanym argumentem -d skript smaze stazene soubory krome titulku s nejvetsi shodou
